from django.shortcuts import render
from librehatti.catalog.models import *

import datetime
from django.db.models import Sum

def bill(request):
    
    pi = PurchasedItem.objects.get(item_id=1)
    po = PurchaseOrder.objects.get(buyer_id=2)

    date= datetime.datetime.now()
    bill_date=po.date_time
    purchaseditem= PurchasedItem.objects.values('item','price','qty')
    item = pi.item
    price=pi.price
    qty =pi.qty
    sub_total= qty*price
         
    delivery_address=po.delivery_address
    organisation=po.organisation
    buyer_id=po.buyer_id
    
    return render(request, 'bill.html', { 'STC_No':'1', 'PAN_No' :'12', 'date': date, 'delivery_address' : delivery_address, 'Organisation' : organisation, 'buyer_id' : buyer_id, 'L_No.': '123', 'bill_date': bill_date, 'purchaseditem' : purchaseditem, 'item' : item, 'price' : price, 'qty':qty, 'total': sub_total} )

