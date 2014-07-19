#from django.http import HttpResponse
#from useraccounts.models import *
#from helper import *
from django import forms
from django.shortcuts import render
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import Surcharge
from django.db.models import Sum

    

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
                    purchased_item, 'total_cost': total,'tax_data': tax_data, 
                   'surcharge_total':surcharge_total, 'grand_total':grand_total
                  })
 
