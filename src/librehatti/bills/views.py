
from django.shortcuts import render
from django.http import HttpResponse 
from librehatti.catalog.models import PurchaseOrder, PurchasedItem
from librehatti.bills.models import *
from django.contrib.auth.models import User
import useraccounts
from django.db.models import Sum
from librehatti.bills.forms import ConfirmForm

def confirm(request,client_id):
    quoted_order = QuotedOrder.objects.get(pk=int(client_id))
    quoted_item = QuotedItem.objects.filter(quote_order_id=int(client_id)).values('quote_item__name', 'quote_qty')
    i_d = quoted_order.quote_buyer_id
    form = ConfirmForm(initial={'quote_item':'item1', 'qty1':'quote_qty'})
    return render(request, 'bills/confform.html', {'quoted_order' : quoted_order,'form':form,
                 'quoted_item' : quoted_item,  'id' : i_d})



def final(request,name):
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            qty1 = request.POST ['quote_qty']
            item1 = request.POST ['quote_item']
            return HttpResponse(qty1,item1)
