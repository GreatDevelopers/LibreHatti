 # Create your views here.

from django.shortcuts import render
from librehatti.catalog.models import *
import datetime
from django.db.models import Sum

def bill(request):
    
    purchased_item = PurchasedItem.objects.get(pk=1)
    purchase_order = PurchaseOrder.objects.get(pk=2)
    purchaseditem= PurchasedItem.objects.values('item','price','qty')
    per_price = purchased_item.item.price
    total=PurchasedItem.objects.filter(id=1).aggregate(Sum('price'))
    date= datetime.datetime.now()
    bill_date=purchase_order.date_time      
    delivery_address=purchase_order.delivery_address
    organisation=purchase_order.organisation
    buyer_id=purchase_order.buyer_id
    
    return render(request, 'bill.html', { 'STC_No':'1', 'PAN_No' :'12',
    'date': date, 'delivery_address' : delivery_address, 
    'Organisation' : organisation,'buyer_id' : buyer_id, 'L_No.': '123',
    'bill_date': bill_date,'purchaseditem' : purchaseditem,'per_price': per_price, 'total_cost': total })

