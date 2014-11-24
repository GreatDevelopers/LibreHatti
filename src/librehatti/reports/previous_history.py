from django.shortcuts import render

from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from django.contrib.auth.decorators import login_required
from librehatti.catalog.request_change import request_notify

@login_required
def history(request):
    """
    displays the purchase history of the client
    """
	
    user_id = request.GET['user_id']
    purchases = PurchaseOrder.objects.filter(buyer__id=user_id)
    request_status = request_notify()
    return render(request,'reports/purchase_history.html',{'purchases':purchases,'request':request_status})

@login_required
def details(request):
    """
    displays the details of the purchase of the client
    """
	
    order_id = request.GET['order_id']
    purchases = PurchasedItem.objects.filter(purchase_order__id=order_id)
    request_status = request_notify()
    return render(request,'reports/history_details.html',{'purchases':purchases,\
        'order_id':order_id,'request':request_status})
