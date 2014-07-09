from django.shortcuts import render
from django.http import HttpResponse 
from librehatti.catalog.models import PurchaseOrder, PurchasedItem
from librehatti.bills.models import *
from django.contrib.auth.models import User
import useraccounts
from django.db.models import Sum
from librehatti.bills.forms import ConfirmForm

def list_quoted(request):
    quoted = QuotedItem.objects.values('quote_order__id','quote_order__quote_buyer_id__username').filter(confirm_status = 0)
    return render(request,'bills/quoted_list.html',{'quoted':quoted}) 

def confirm(request):
    if request.method == "POST":
	form = ConfirmForm(request.POST)
        if form.is_valid:
            client = User.objects.get(id = request.GET['client'])
            quote_qty = request.POST["quote_qty"]
            quote_item = request.POST["quote_item"]
            return HttpResponse(client)
    else:
        quote_order_id = request.GET['id']
        quoted_item = QuotedItem.objects.filter(quote_order_id = quote_order_id).values('quote_item__name', 'quote_qty','quote_discount')
        client_id = QuotedOrder.objects.values("quote_buyer_id__id").filter(id = quote_order_id)
        form = ConfirmForm(initial={'quote_item':'item1', 'qty1':'quote_qty'})
        return render(request, 'bills/confform.html', {'form':form,'client_id':client_id,
                 'quoted_item' : quoted_item})
