from django.http import HttpResponse
from django.shortcuts import render
from librehatti.catalog.models import Category
from librehatti.catalog.models import Product
from librehatti.catalog.forms import AddCategory,TransportForm1,TransportForm2
from librehatti.catalog.models import Transport
from django.db.models import Sum
from librehatti.prints.helper import num2eng
from librehatti.catalog.forms import ItemSelectForm
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
    return render(request,'index.html',{})


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


def transport(request):
    form = TransportForm1()
    temp = {'TransportForm':form}
    return render (request, 'bills/form.html',temp)


def transport_bill(request):
    if request.method == 'POST':
        form = TransportForm1(request.POST)
        if form.is_valid():
           
            if 'button1' in request.POST:
                    vehicle_id = request.POST['vehicle_id']
                    job_id = request.POST['job_id']
                    kilometer = float(request.POST['kilometer'])          
                    date = request.POST['date']
                    rate = float(request.POST['rate'])
                    total = rate*kilometer
                    obj = Transport(vehicle_id=vehicle_id, job_id=job_id, 
                           kilometer=kilometer, Date=date, rate=rate, 
                           total=total) 
                    obj.save()
                    temp = Transport.objects.filter(job_id=obj.job_id)
                    total_amount = Transport.objects.filter(job_id=obj.job_id
                           ).aggregate(Sum('total')).get('total__sum', 0.00)
                    return render(request,'bills/transport_bill.html', 
                           {'temp' : temp, 'words' : num2eng(total_amount), 
                            'total_amount' : total_amount}) 

            else:
                    vehicle_id = request.POST['vehicle_id']
                    job_id = request.POST['job_id']
                    kilometer = float(request.POST['kilometer'])
                    date = request.POST['date']
                    rate = float(request.POST['rate'])
                    total = rate * kilometer
                    obj = Transport(vehicle_id=vehicle_id, job_id=job_id, 
                                    kilometer=kilometer, Date=date, rate=rate, 
                                    total=total) 
                    obj.save()
                         
    else:
        form = TransportForm1()
    return render(request, 'bills/form.html', {'TransportForm':form}) 

"""
This view allows filtering of sub category according to parent category of 
item.
"""
def select_sub_category(request):
    parent_category = request.GET['cat_id']
    sub_categories = Category.objects.filter(parent=parent_category)
    sub_category_dict = {}
    for sub_category in sub_categories:
        sub_category_dict[sub_category.id] = sub_category.name
    return HttpResponse(simplejson.dumps(sub_category_dict))

"""
This view allows filtering of item according to sub category of item.
"""
def select_item(request):
    cat_id = request.GET['cat_id']
    products = Product.objects.filter(category = cat_id)
    product_dict = {}
    for product in products:
        product_dict[product.id] = product.name
    return HttpResponse(simplejson.dumps(product_dict))     
  
