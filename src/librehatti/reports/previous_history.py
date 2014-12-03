from django.shortcuts import render
from django.http import HttpResponse

from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from django.contrib.auth.decorators import login_required
from librehatti.catalog.request_change import request_notify
from librehatti.voucher.models import VoucherId

@login_required
def history(request):
    """
    displays the purchase history of the client
    """
	
    user_id = request.GET['user_id']
    purchases = VoucherId.objects.values('purchase_order','purchase_order_of_session',\
        'purchase_order__mode_of_payment__method','purchase_order__date_time').\
        filter(purchase_order__buyer__id=user_id)
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
