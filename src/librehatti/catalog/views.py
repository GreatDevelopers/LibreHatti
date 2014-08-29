from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from librehatti.catalog.models import Category
from librehatti.catalog.models import Product
from librehatti.catalog.models import *
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
    form = TransportFormA()
    form1 = TransportFormB()
    temp = {'TransportFormA':form} #'TransportFormB':form1}
    return render (request, 'catalog/form.html',temp)


def transport_bill(request):
    if request.method == 'POST':
        form = TransportFormA(request.POST)
        form1 = TransportFormB(request.POST)
        if form.is_valid() or form1.is_valid():

            if form1.is_valid():
                i = Transport.objects.all().aggregate(Max('id'))
                j= i['id__max']
                form = TransportFormB(request.POST)
                
                if form.is_valid():  
                    cd = form.cleaned_data
                    vehicle = Transport.objects.get(id=j)
                    vehicle_id = vehicle.vehicle_id
                    job_id = vehicle.job_id
                    rate = vehicle.rate             
                    kilometer = float(cd['kilometer'])
                    date = request.POST['Date']
                    total = rate * kilometer
                    obj = Transport(vehicle_id=vehicle_id, job_id=job_id, 
                           kilometer=kilometer, Date=date, rate=rate, 
                           total=total) 
                    obj.save()

                    if 'button1' in request.POST:
                        temp = Transport.objects.filter(job_id=vehicle.job_id)
                        total_amount = Transport.objects.filter(
                                       job_id=vehicle.job_id).aggregate(
                                       Sum('total')).get('total__sum', 0.00)
                        return render(request,'catalog/transport_bill.html', 
                               {'temp' : temp, 'words' : num2eng(total_amount), 
                                'total_amount' : total_amount, 
                                'date':datetime.datetime.now()})

                else:
                    form = TransportFormB()
                    return render(request, 'catalog/form.html', {
                           'TransportFormB':form})


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
            form1 = TransportFormB()
            temp = {'TransportFormA':form, 'TransportFormB':form1}
        return render(request, 'catalog/form.html', temp)


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
    purchase_order = PurchaseOrder.objects.get(id=purchase_order_id)
    purchase_item = PurchasedItem.objects.\
    filter(purchase_order=purchase_order_id).aggregate(Sum('price'))
    price_total = purchase_item['price__sum']
    surcharge = Surcharge.objects.values('id','value')
    for value in surcharge:
        surcharge_id = value['id']
        surcharge_value = value['value']
        taxes = (price_total * surcharge_value)/100
        surcharge_obj = Surcharge.objects.get(id=surcharge_id)
        taxes_applied = TaxesApplied(purchase_order = purchase_order,
        surcharge = surcharge_obj, tax = taxes)
        taxes_applied.save()
    taxes_applied_obj = TaxesApplied.objects.\
    filter(purchase_order=purchase_order_id).aggregate(Sum('tax'))
    tax_total = taxes_applied_obj['tax__sum']
    grand_total = price_total + tax_total
    bill = Bill(purchase_order = purchase_order, total_cost = price_total,
    total_tax = tax_total, grand_total = grand_total)
    bill.save()
    request.session['old_post'] = old_post
    request.session['purchase_order_id'] = purchase_order_id
    return HttpResponseRedirect('/suspense/add_distance/')       

