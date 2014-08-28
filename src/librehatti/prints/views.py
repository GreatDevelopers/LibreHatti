#from django.http import HttpResponse
#from useraccounts.models import *
#from helper import *
from django import forms
from django.shortcuts import *
from librehatti.catalog.models import *
from django.db.models import Sum
import simplejson
from forms import LabReportForm

def lab_report(request):
    """
    It generates the report which lists all the orders for the test 
    selected and the in the entered Time Span.
    """
    category = request.GET['sub_category']
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    purchase_item = PurchasedItem.objects.filter(purchase_order__date_time__range
        =(start_date,end_date),item__category=category).values(
        'purchase_order_id','purchase_order__date_time',
        'purchase_order__buyer_id__username',
        'purchase_order__buyer_id__customer__title',
        'purchase_order__buyer_id__customer__company','price',
        'purchase_order__buyer_id__customer__is_org')
    category_name = Category.objects.values('name').filter(id=category)
    
    total = PurchasedItem.objects.filter(purchase_order__date_time__range 
        = (start_date,end_date),item__category=category).\
        aggregate(Sum('price')).get('price__sum', 0.00)
    
    return render(request, 'prints/lab_reports.html', { 'purchase_item':
                   purchase_item,'start_date':start_date,'end_date':end_date,
                  'total_cost':total,'category_name':category_name})

def show_form(request):
    """
    This view is to show the form for Lab Report.
    """
    if request.method == 'POST':
        form = LabReportForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
         form = LabReportForm()
    return render(request, 'prints/show_form.html', {
              'form':form
    })
    
def filter_sub_category(request):
    """
    This view filters the sub_category according to the parent_category.
    """
    parent_category = request.GET['parent_id']
    sub_categories = Category.objects.filter(parent=parent_category)
    sub_category_dict = {}
    for sub_category in sub_categories:
        sub_category_dict[sub_category.id] = sub_category.name
    return HttpResponse(simplejson.dumps(sub_category_dict))

def bill(request):   
    """
    It generates a Bill for the user which lists all the items, 
    their quantity , subtotal and then adds it to the surcharges
    and generates the Grand total.
    """
    id = request.GET['order_id']
    purchase_order = PurchaseOrder.objects.filter(id = id)
    purchased_item = PurchasedItem.objects.filter(purchase_order_id = id).values(
    'item__name', 'qty','item__price_per_unit','price') 
    total = PurchasedItem.objects.filter(purchase_order_id=id).aggregate(Sum(
    'price')).get('price__sum', 0.00)
    # TODO:
    # Surcharges and Grand Total are not yet there. Data will come
    # from Bills table. Amrit and Aseem are working on it.
    return render(request, 'prints/bill.html', { 'STC_No' :'1','PAN_No' :'12', 'L_No':
                 '123', 'purchase_order':purchase_order, 'purchased_item' : 
                 purchased_item, 'total_cost': total})
