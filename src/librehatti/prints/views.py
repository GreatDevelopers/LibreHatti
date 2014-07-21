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
    purchase_order = PurchaseOrder.objects.all()
    purchased_item = PurchasedItem.objects.filter().values('item__name', 'qty',
                     'item__price_per_unit','price') 
    total = PurchasedItem.objects.filter().aggregate(Sum('price')).get( 
                                                     'price__sum', 0.00)
    surcharge = Surcharge.objects.filter().values('tax_name' ,'value')
    surcharge_total=0
    i=0 
    tax_list = []
    tax_data = []	
    for tax in surcharge:
        tax_list.append(float((tax['value']*total)/100))
    
    for tax in tax_list:
        surcharge_total=surcharge_total+tax	        
        tax_data = zip(surcharge, tax_list)
    grand_total = surcharge_total  + total
    return render(request, 'bill.html', { 'STC_No' :'1','PAN_No' :'12', 'L_No':
                 '123', 'purchase_order':purchase_order, 'purchased_item' : 
                 purchased_item, 'total_cost': total,'surcharge_total':
                 surcharge_total, 'tax_data' : tax_data, 'grand_total':
                 grand_total})
