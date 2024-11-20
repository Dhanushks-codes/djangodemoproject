from django.shortcuts import render,redirect
from movie.models import Movie

# Create your views here.
def home(request):
    k=Movie.objects.all()
    context={'movie':k}
    return render(request,'home.html',context)


def addmovies(request):
    if (request.method=="POST"):
        t=request.POST['t']
        d=request.POST['d']
        y=request.POST['y']
        l=request.POST['l']
        c=request.FILES['c']
        b=Movie.objects.create(title=t,description=d,year=y,language=l,cover=c)
        b.save()
        return redirect('home')

    return render(request,'addmovies.html')
def details(request,p):
    m=Movie.objects.get(id=p)
    context={'movie':m}
    return render(request,'details.html',context=context)
def delete(request,p):
    m=Movie.objects.get(id=p)
    m.delete()
    return redirect('home')
def edit(request,p):
    m=Movie.objects.get(id=p)
    if (request.method=="POST"):
        m.title=request.POST['t']
        m.description=request.POST['d']
        m.year=request.POST['y']
        m.language=request.POST['l']
        if(request.FILES.get('c')==None):
            m.save()
        else:
            m.cover=request.FILES['c']
        m.save()
        return redirect('home')
    context = {'movie': m}
    return render(request, 'edit.html', context=context)
