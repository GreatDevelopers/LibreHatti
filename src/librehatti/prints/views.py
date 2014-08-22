#from django.http import HttpResponse
#from useraccounts.models import *
#from helper import *
from django import forms
from django.shortcuts import *
from librehatti.catalog.models import *
from django.db.models import Sum

    
def add_lab(request):
    """
    It displays the form where the user selects the Lab.
    """
    lab_info = Category.objects.all()

    return render(request,'prints/add_lab.html',{'lab_info':lab_info})

def add_material(request):
    """
    Depending on the Lab selected, this function displays the form where
    the user selects Material.
    """
    lab = request.GET['lab']
    material_info = Category.objects.filter(parent__name=lab)
    return render( request, 'prints/add_material.html', {'lab':lab, 
                  'material_info' : material_info}) 
 


def add_test(request):
    """
    Depending on the Lab and Material selected, this function displays
    the form where the user selects a test and enters the time span.
    """
    if 'Submit' in request.GET:
        material = request.GET['material']
        
        test_info = Product.objects.filter(category__name=material)
        return render( request, 'prints/add_test.html', {
                      'material':material,'test_info' : test_info})
        
def lab_report(request):
    """
    It generates the report which lists all the orders for the test 
    selected and the in the entered Time Span.
    """
    test = request.POST['test']
    start_date = request.POST['From']
    end_date = request.POST['To']
    purchase_item= PurchasedItem.objects.filter(purchase_order__date_time__range
                  =(start_date,end_date),item__name=test).values( 
                    'purchase_order_id','purchase_order__date_time',
                   'purchase_order__buyer_id__username',
                  'purchase_order__buyer_id__customer__title',
                  'purchase_order__buyer_id__customer__company','price',
                  'purchase_order__buyer_id__customer__is_org')
    
    total=PurchasedItem.objects.filter(purchase_order__date_time__range 
        =(start_date,end_date)).aggregate(Sum('price')).get('price__sum', 0.00)
    return render(request, 'prints/lab_reports.html', { 'purchase_item':
                   purchase_item,'start_date':start_date,'end_date':end_date,
                  'total_cost':total})

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
