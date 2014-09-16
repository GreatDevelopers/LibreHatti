from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Sum

from librehatti.catalog.models import Category
from librehatti.catalog.models import Product
from librehatti.catalog.models import *
from librehatti.catalog.forms import AddCategory,TransportFormA,TransportFormB
from librehatti.catalog.models import Transport
from librehatti.catalog.forms import ItemSelectForm

from librehatti.prints.helper import num2eng

from librehatti.suspense.models import SuspenseOrder

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


def transport_bill(request):
    if request.method == 'POST':
        form = TransportFormA(request.POST)
        form1 = TransportFormB(request.POST)
       
        if form.is_valid() or form1.is_valid():
 
          if form1.is_valid():
                i = Transport.objects.all().aggregate(Max('id'))
                j= i['id__max']
                
                #vehicle_id = Transport.objects.filter(id=j).values('vehicle_id')
                #job_id = Transport.objects.filter(id=j).values('job_id')
                #rate = Transport.objects.filter(id=j).values('rate')
                #if 'button2' in request.POST:
 
                if form.is_valid():  
                    cd = form.cleaned_data
                    vehicle = Transport.objects.get(id=j)
                    #for i in vehicle:
                    #ListDict = {'vehicle_id':i.vehicle_id, 'job_id':i.job_id, 'rate':i.rate }
                    vehicle_id = vehicle.vehicle_id
                    job_id = vehicle.job_id
                    rate = vehicle.rate
                    #vehicle_id = obj.vehicle_id               
                    kilometer = float(cd['kilometer'])
                    date = request.POST['Date']
                    total = rate * kilometer
                    obj = Transport(vehicle_id=vehicle_id, job_id=job_id, 
                           kilometer=kilometer, Date=date, rate=rate, 
                           total=total) 
                    obj.save()
                    #return render(request,'catalog/transport_bill.html', 
                    #          {'v':v}) 
 
                    if 'button1' in request.POST:
                     temp = Transport.objects.filter(job_id=vehicle.job_id)
                     total_amount = Transport.objects.filter(job_id=vehicle.job_id
                             ).aggregate(Sum('total')).get('total__sum', 0.00)
                     return render(request,'catalog/transport_bill.html', 
                           {'temp' : temp, 'words' : num2eng(total_amount), 
                            'total_amount' : total_amount, 
                            'date':datetime.datetime.now()})
 
                else:
                     form = TransportFormB()
                     return render(request, 'catalog/transport.html', {'TransportFormB':form})
 
 
          elif form.is_valid():
            cd = form.cleaned_data
            form = TransportFormA(request.POST)
            vehicle_id = cd['vehicle_id']
            
            job_id = cd['job_id']
            
            kilometer = float(cd['kilometer'])
            date = request.POST['Date']
            rate = float(cd['rate'])
            
            total = rate * kilometer
            obj = Transport(vehicle_id=vehicle_id, job_id=job_id, 
                           kilometer=kilometer, Date=date, rate=rate, 
                           total=total) 
            obj.save()
            
            if 'button1' in request.POST:
                temp = Transport.objects.filter(job_id=obj.job_id)
                total_amount = Transport.objects.filter(job_id=obj.job_id
                             ).aggregate(Sum('total')).get('total__sum', 0.00)
                return render(request,'catalog/transport_bill.html', 
                           {'temp' : temp, 'words' : num2eng(total_amount), 
                            'total_amount' : total_amount, 
                            'date':datetime.datetime.now()}) 
                
                                             
        else:
            form = TransportFormA()
            form = TransportFormB()
        temp = { 'TransportFormB':form1}
        return render(request, 'catalog/transport.html', temp)  




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


"""
This view calculate taxes on purchased order, bill data
and save those values in database.
"""
def bill_cal(request):
    old_post = request.session.get('old_post')
    purchase_order_id = request.session.get('purchase_order_id')

    suffix = "/search_result/?search="
    prefix = "&Order=Order+Search"
    url = suffix + str(purchase_order_id) + prefix

    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    purchase_order_obj = PurchaseOrder.objects.values('total_discount','tds').get(id=purchase_order_id)
    purchase_item = PurchasedItem.objects.\
    filter(purchase_order=purchase_order_id).aggregate(Sum('price'))
    total = purchase_item['price__sum']
    price_total = total - purchase_order_obj['total_discount']
    surcharge = Surcharge.objects.values('id','value','taxes_included')
    delivery_rate = Surcharge.objects.values('value').filter(tax_name = 'Transportation')
    distance = SuspenseOrder.objects.filter(purchase_order = purchase_order_id).\
        aggregate(Sum('distance_estimated'))
    if distance['distance_estimated__sum']:
        delivery_charges = int(distance['distance_estimated__sum'])*\
            delivery_rate[0]['value']

    else:
        delivery_charges = 0

    for value in surcharge:
        surcharge_id = value['id']
        surcharge_value = value['value']
        surcharge_tax = value['taxes_included']
        if surcharge_tax == 1:
            taxes = (price_total * surcharge_value)/100
            surcharge_obj = Surcharge.objects.get(id=surcharge_id)
            taxes_applied = TaxesApplied(purchase_order = purchase_order,
            surcharge = surcharge_obj, tax = taxes)
            taxes_applied.save()
    taxes_applied_obj = TaxesApplied.objects.\
    filter(purchase_order=purchase_order_id).aggregate(Sum('tax'))
    tax_total = taxes_applied_obj['tax__sum']
    grand_total = price_total + tax_total + delivery_charges
    amount_received = grand_total - purchase_order_obj['tds']
    bill = Bill(purchase_order = purchase_order, total_cost = price_total,
    total_tax = tax_total, grand_total = grand_total,
    delivery_charges = delivery_charges, amount_received = amount_received)
    bill.save()
    request.session['old_post'] = old_post
    request.session['purchase_order_id'] = purchase_order_id
    return HttpResponseRedirect(url)

def list_products(request):
    all_products = Product.objects.all()
    all_categories=Category.objects.all().order_by('name')
    products_dict = { }
    for one_category in all_categories:
        if one_category.is_leaf_node():
            one_category_dict = {}
            products_list = Product.objects.filter(category=one_category)
            attributes_dict = { }
            for one_product in products_list:
                attributes_list = Catalog.objects.filter(product = one_product)
                attributes_dict[one_product] = attributes_list
            one_category_dict[one_category.name] = attributes_dict
            products_dict[one_category.id] = one_category_dict
    return render(request,'list_products.html',{'nodes':all_categories, 'products_dict':products_dict})
