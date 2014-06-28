 # Create your views here.

from django.shortcuts import render
from librehatti.catalog.models import *
from django.db.models import Sum

def bill(request):
    purchase_order = PurchaseOrder.objects.get(buyer_id_id=5)
    purchased_item = PurchasedItem.objects.filter(purchase_order_id=5).values(
    'item__name' ,'qty','item__price','price')	
    total = PurchasedItem.objects.filter(purchase_order_id=5).aggregate(Sum('price')).get('price__sum', 0.00)
    return render(request, 'bill.html', { 'STC_No' :'1','PAN_No' :'12', 'L_No': '123',
     'purchase_order':purchase_order, 'purchased_item' : purchased_item,
     'total_cost': total  })

