from django.http import HttpResponse
from django.shortcuts import render
from librehatti.catalog.models import *
from librehatti.catalog.forms import *

def index(request):
        error = {}
        categorylist = category.objects.all()
        if categorylist.count() == 0:
                nocategory = True
                return render(request, 'catalog.html', {'nocategory': 
                       nocategory})
        productlist = product.objects.all();
        if productlist.count() == 0:
                noproduct = True
                return render(request, 'catalog.html', {'noproduct': noproduct})
        return render(request,'catalog.html', {'productlist': productlist, 
               'categorylist': categorylist})
        pass

def addCategories(request):
        if request.method == 'POST' :
                form = addCategory(request.POST)
                if form.is_valid():
                        return HttpResponseRedirec('/')
        else:
                form = addCategory()

        return render(request, 'addCategory.html', {
                'form':form,
        })
