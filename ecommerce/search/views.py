from django.shortcuts import render
from django.db.models import Q
from shop.models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required()
def search(request):

    if (request.method=="POST"):
        query = request.POST['p']
        b = None
        # print(query)
        if (query):
            b = Product.objects.filter(Q(name__icontains=query))
            context = {"product":b}
    return render(request,'searchresults.html',context)
