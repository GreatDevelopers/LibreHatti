from django.http import HttpResponse
from django.shortcuts import render
from librehatti.catalog.models import Category
from librehatti.catalog.models import Product
from librehatti.catalog.forms import AddCategory



def index(request):
    """
    It lists all the products and the user can select any product
    and can add them to the cart.
    """
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
    """
    It allows the user to add categories. 
    """

    if request.method == 'POST' :
        form = AddCategory(request.POST)
        if form.is_valid():
            return HttpResponseRedirec('/')
    else:
        form = AddCategory()
    return render(request, 'addCategory.html', {
            'form':form
    })
