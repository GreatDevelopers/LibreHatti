from django.shortcuts import render

from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from django.contrib.auth.decorators import login_required


@login_required
def history(request):
    """
    displays the purchase history of the client
    """
	
    user_id = request.GET['user_id']
    purchases = PurchaseOrder.objects.filter(buyer__id=user_id)
    return render(request,'reports/purchase_history.html',{'purchases':purchases})

@login_required
def details(request):
    """
    displays the details of the purchase of the client
    """
	
    order_id = request.GET['order_id']
    purchases = PurchasedItem.objects.filter(purchase_order__id=order_id)
    return render(request,'reports/history_details.html',{'purchases':purchases})
