from django.http import HttpResponse
from django.shortcuts import render
from librehatti.catalog.models import Category
from librehatti.catalog.models import Product
from librehatti.catalog.forms import AddCategory
import simplejson

def index(request):
    """
    It lists all the products and the user can select any product
    and can add them to the cart.
    """
    """error = {}
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

    pass"""
    return render(request,'index.html')


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

def select_secondary_category(request):
    lab = request.GET['cat_id']
    materials = Category.objects.filter(parent=lab)
    material_dict = {}
    for material in materials:
        material_dict[material.id] = material.name
    return HttpResponse(simplejson.dumps(material_dict))

def select_item(request):
    cat_id = request.GET['cat_id']
    products = Product.objects.filter(category = cat_id)
    product_dict = {}
    for product in products:
        product_dict[product.id] = product.name
    return HttpResponse(simplejson.dumps(product_dict))
