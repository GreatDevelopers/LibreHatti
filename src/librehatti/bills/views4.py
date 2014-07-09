from django.shortcuts import render
from django.http import HttpResponseRedirect 
from librehatti.catalog.models import PurchaseOrder, PurchasedItem
from librehatti.bills.models import *
from django.contrib.auth.models import User
import useraccounts
from django.db.models import Sum

def confirm(request,client_id):

    quoted_order = QuotedOrder.objects.get(pk=int(client_id))
    quoted_item = QuotedItem.objects.filter(quote_order_id=int(client_id)).values_list('quote_item__name', 'quote_qty', 'quote_price')
    total_cost = QuotedItem.objects.filter(quote_order_id=int(client_id)).aggregate(Sum('quote_price')).get('price__sum', 0.00)
    i_d = quoted_order.quote_buyer_id
    return render(request, 'bills/confform.html', {'quoted_order' : quoted_order, 
                 'quoted_item' : quoted_item, 'total_cost' : total_cost, 'id' : i_d})



def final(request,name):
   if request.method=='POST':
        a = ConfirmForm(request.POST)
        if a.is_valid():
            cd = a.cleaned_data
            quote_item = cd['quote_item'] 
            quote_qty = cd['quote_qty']
            obj = PurchasedItem.objects.create(item__name=quote_item,qty=quote_qty)
            obj = PurchasedItem(item__name=quote_item,qty=quote_qty)
            obj.save()
            quoted_order = QuotedOrder.objects.get(pk=name)
            quoted_item = QuotedItem.objects.filter(quote_order_id=name).values_list('quote_item__name', 'quote_qty', 'quote_price')
            total_cost = QuotedItem.objects.filter(quote_order_id=name).aggregate(Sum('quote_price')).get('price__sum', 0.00)
            return render(request, 'bills/bills.html', {'quoted_order' : quoted_order, 
                 'quoted_item' : quoted_item, 'total_cost' : total_cost, 'form':form })
   else:
        form = ConfirmForm()		
   return render(request,'bills/bills.html')


