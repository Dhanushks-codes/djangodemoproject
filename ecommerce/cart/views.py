from django.shortcuts import render, redirect
from shop.models import Product
from cart.models import Cart, Payment, Order_details

import razorpay


# Create your views here.
def addtocart(request, i):
    print(i)
    p = Product.objects.get(id=i)
    u = request.user
    try:
        c = Cart.objects.get(user=u, product=p)
        c.quantity += 1
        p.stock -= 1
        p.save()
        c.save()
    except:
        c = Cart.objects.create(product=p, user=u, quantity=1)
        p.stock -= 1
        p.save()
        c.save()

    return redirect('cart:cartview')


def cart_view(request):
    u = request.user
    c = Cart.objects.filter(user=u)
    total = 0
    for i in c:
        total += i.quantity * i.product.price
    context = {'cart': c, 'total': total}
    return render(request, 'cart.html', context)


def deduct(request, i):
    u = request.user
    p = Product.objects.get(id=i)
    c = Cart.objects.get(user=u, product=p)
    if (c.quantity > 1):
        c.quantity -= 1
        c.save()
        p.stock += 1
        p.save()
    else:
        c.delete()
        p.stock += 1
        p.save()
    return redirect('cart:cartview')


def removeitem(request, i):
    u = request.user
    p = Product.objects.get(id=i)
    try:
        c = Cart.objects.get(user=u, product=p)

        c.delete()
        p.stock += c.quantity
        p.save()
    except:
        pass
    return redirect('cart:cartview')


def place_order(request):
    if request.method == "POST":
        ad = request.POST['ad']
        ph = request.POST['ph']
        pi = request.POST['pi']
        u = request.user
        c = Cart.objects.filter(user=u)
        total = 0
        for i in c:
            total += i.quantity * i.product.price
        print("total", total)

        # razorpay connection
        client = razorpay.Client(auth=('rzp_test_Puu7HlvS2Pdev7', 'Q0SdJkgKbKxaiAWXkz5R80wR'))
        # razorpay order creation
        response_payment = client.order.create(dict(amount=total * 100, currency='INR'))
        # print(response_payment)
        order_id = response_payment['id']
        status = response_payment['status']
        if status == 'created':
            p = Payment.objects.create(name=u.username, amount=total, order_id=order_id)
            p.save()
            for i in c:
                o = Order_details.objects.create(product=i.product, user=i.user, order_id=order_id, phone=ph, pin=pi,
                                                 address=ad, no_of_items=i.quantity)
                o.save()

            context = {'payment': response_payment, 'name': u.username}
            return render(request, 'payment.html', context)
    return render(request, 'placeorder.html')


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login


@csrf_exempt
def payment_status(request, p):
    user = User.objects.get(username=p)
    login(request, user)

    response = request.POST
    print(response)
    param_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_signature': response['razorpay_signature']

    }

    client = razorpay.Client(auth=('rzp_test_Puu7HlvS2Pdev7', 'Q0SdJkgKbKxaiAWXkz5R80wR'))
    try:
        status = client.utility.verify_payment_signature(param_dict)
        print(status)
        p = Payment.objects.get(order_id=response['razorpay_order_id'])
        p.razorpay_payment_id = response['razorpay_payment_id']
        p.paid = True
        p.save()

        o = Order_details.objects.filter(order_id=response['razorpay_order_id'])
        for i in o:
            i.payment_status = "completed"
            i.save()
        c=Cart.objects.filter(user=user)
        c.delete()
    except:
        pass
    return render(request, 'payment_status.html')
def order_view(request):
    u=request.user
    o=Order_details.objects.filter(user=u,payment_status="completed")
    print(o)
    context={'orders':o}
    return render(request,'orders.html',context)