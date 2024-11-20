from django.shortcuts import render,redirect,get_object_or_404
from shop.models import Category,Product
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
# Create your views here.
def categories(request):
    k = Category.objects.all()
    context = {'Category': k}
    return render(request,'categories.html',context)
@login_required()
def products(request,i):
    c=Category.objects.get(id=i)
    p=Product.objects.filter(category=c)
    context={'cat':c,'pro':p}
    return render(request,'product.html',context)

def productdetail(request,i):
    p=Product.objects.get(id=i)
    context={'pro':p}
    return render(request,'details.html',context)
def register(request):
        if (request.method == "POST"):
            u = request.POST['u']
            p = request.POST['p']
            cp = request.POST['cp']
            e = request.POST['e']
            f = request.POST['f']
            l = request.POST['l']
            if (p == cp):
                u = User.objects.create_user(username=u, password=p, email=e, first_name=f, last_name=l)
                u.save()
            else:
                return HttpResponse("Passwords must be same")
            return redirect('shop:categories')
        return render(request,'register.html')

def user_login(request):
    if (request.method == "POST"):
        u = request.POST['u']
        p = request.POST['p']

        user = authenticate(username=u, password=p)
        if user:
            login(request,user)
            return redirect('shop:categories')
        else:
            return HttpResponse("Invalid credentials")

    return render(request,'login.html')
def userlogout(request):
    logout(request)
    return redirect('shop:categories')

#add categories
def add_category(request):
    if (request.method == "POST"):
        n = request.POST['n']
        d = request.POST['d']
        i = request.FILES['i']
        b = Category.objects.create(name=n,desc=d, image=i)
        b.save
        return redirect('shop:categories')
    return render(request,'add_category.html')
def add_product(request):
    if (request.method == "POST"):
        catid = request.POST.get('cat')
        pro = request.POST['pro']
        d = request.POST['d']
        p = request.POST['p']
        s = request.POST['s']
        i = request.FILES.get('i')
        cat=Category.objects.get(id=catid)
        b=Product.objects.create(name=pro,desc=d,price=p,stock=s,image=i,category=cat)
        b.save
        return redirect('shop:categories')
    return render(request,'add_product.html')

def add_stock(request,id):
    p=Product.objects.get(id=id)
    context={'pro':p}
    if(request.method=="POST"):
        p.stock=request.POST['n']
        p.save()
        return redirect('shop:detail',id)

    return  render(request,'add_stock.html',context)
