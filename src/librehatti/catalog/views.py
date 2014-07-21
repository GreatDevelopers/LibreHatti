from django.http import HttpResponse
from django.shortcuts import render
from librehatti.catalog.models import *
from librehatti.catalog.forms import *


def index(request):
    error = {}
    categorylist = Category.objects.all()

    if categorylist.count() == 0:
        nocategory = True
        return render(request, 'catalog.html', {'nocategory': nocategory})
    productlist = Product.objects.all();

    if productlist.count() == 0:
        noproduct = True
        return render(request, 'catalog.html', {'noproduct': noproduct})

    return render(request,'catalog.html', {'productlist': productlist, 
               'categorylist': categorylist})

    pass


def add_categories(request):

    if request.method == 'POST' :
        form = addCategory(request.POST)
        if form.is_valid():
            return HttpResponseRedirec('/')
    else:
        form = addCategory()
    return render(request, 'addCategory.html', {
            'form':form,
    })
