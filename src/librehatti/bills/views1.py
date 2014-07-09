from django.shortcuts import render
from django.http import HttpResponseRedirect 
from librehatti.catalog.models import PurchaseOrder, PurchasedItem
from librehatti.bills.models import *
from django.contrib.auth.models import User
import useraccounts
from django.db.models import Sum

def confirm(request):
  
    error = False
    if 'quote_item' in request.GET:
        item1 = request.GET['quote_item']
        qty1 = request.GET['quote_qty']
        if not (item1 or qty1):
            error = True
            quoted_item = QuotedItem.objects.filter(pk=1)
            quoted_qty = QuotedItem.quote_qty

        else:   
            quoted_order = QuotedOrder.objects.filter(pk=1)
            quoted_item = QuotedItem.objects.filter(pk=1)
            total = QuotedItem.objects.filter(id=1).aggregate(Sum('price'))
            #obj = PurchaseOrder.objects.get(id=1)
            #obj.save()
            
            value = QuotedItem.objects.filter(quote_item=item1)
            value1 = QuotedItem.objects.filter(quote_qty=qty1)
   
            return render(request, 'bills/bills.html',
 {'item1': quoted_item, 'qty1': quoted_qty})

    return render(request,'bills/confform.html', {'error':error})   

      


