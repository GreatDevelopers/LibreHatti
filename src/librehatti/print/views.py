 # Create your views here.

from django.shortcuts import render
from librehatti.catalog.models import *
import datetime
from django.db.models import Sum

def bill(request):
    
    purchased_item = PurchasedItem.objects.get(item_id=1)
    purchase_order = PurchaseOrder.objects.get(buyer_id=2)
    date= datetime.datetime.now()
    bill_date=purchase_order.date_time
    purchaseditem= PurchasedItem.objects.values('item','price','qty')
    sub_total= purchased_item.qty * purchased_item.price        
    delivery_address=purchase_order.delivery_address
    organisation=purchase_order.organisation
    buyer_id=purchase_order.buyer_id
    
    return render(request, 'bill.html', { 'STC_No':'1', 'PAN_No' :'12',
    'date': date, 'delivery_address' : delivery_address, 
    'Organisation' : organisation,'buyer_id' : buyer_id, 'L_No.': '123',
    'bill_date': bill_date,'purchaseditem' : purchaseditem, 'total':sub_total})