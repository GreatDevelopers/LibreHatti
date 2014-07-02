
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
    quoted_item = QuotedItem.objects.filter(quote_order_id=int(client_id)).values_list('quote_item__name', 'quote_qty', 'quote_price')
    total_cost = QuotedItem.objects.filter(quote_order_id=int(client_id)).aggregate(Sum('quote_price')).get('price__sum', 0.00)
    i_d = quoted_order.quote_buyer_id
    return render(request, 'bills/confform.html', {'quoted_order' : quoted_order, 
                 'quoted_item' : quoted_item, 'total_cost' : total_cost, 'id' : i_d})



def final(request,name):
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            p_item(
                  cd['quote_item'],
                  cd['quote_qty'],
                  cd.get('quote_item','quote_qty'),
                  ['item__name','qty'],
            )
            total_cost = PurchasedItem.objects.filter     (quote_order_id=int(client_id)).aggregate(Sum('price')).get('price__sum', 0.00)
            return render(request, 'bills/p_bill.html', {'total_cost' : total_cost, 'form':form })
        else:
             form = ConfirmForm(
                initial={'quote_item':'quote_item', 'quote_qty':'quote_qty'}
             )
             client_id = 1
             quoted_order = QuotedOrder.objects.get(pk=int(client_id))
             quoted_item = QuotedItem.objects.filter(quote_order_id=int(client_id)).values_list('quote_item__name', 'quote_qty', 'quote_price')
             total_cost = QuotedItem.objects.filter(quote_order_id=int(client_id)).aggregate(Sum('quote_price')).get('price__sum', 0.00)
             i_d = quoted_order.quote_buyer_id
             form = ConfirmForm()
             return render(request, 'bills/p_bill.html', {'quoted_order' : quoted_order, 
                 'quoted_item' : quoted_item, 'total_cost' : total_cost, 'id' : i_d,'form':form})
      

             #return render(request, 'bills/bills.html')


            #quote_item = request.POST['quote_item']
            #quote_qty = request.POST['quote_qty']
            #a.item = Product.objects.get(name=quote_item)
            #a.purchase_order = PurchasedItem.objects.get(pk=name)
            #a.save()
            #purchase_order = PurchaseOrder.objects.get(pk=name)
            #item = PurchasedItem.objects.filter(purchase_order_id=name).values_list('item__name', 'qty', 'price')
            #total_cost = PurchasedItem.objects.filter(purchase_order_id=name).aggregate(Sum('price')).get('price__sum', 0.00)
            #return render(request, 'bills/bills.html', {'purchase_order' : purchase_order, 
                 #'item' : item, 'total_cost' : total_cost, 'form':form })
    #else:
        #client_id = 1
        #quoted_order = QuotedOrder.objects.get(pk=int(client_id))
        #quoted_item = QuotedItem.objects.filter(quote_order_id=int(client_id)).values_list('quote_item__name', 'quote_qty', 'quote_price')
        #total_cost = QuotedItem.objects.filter(quote_order_id=int(client_id)).aggregate(Sum('quote_price')).get('price__sum', 0.00)
        #i_d = quoted_order.quote_buyer_id
        #form = ConfirmForm()
        #return render(request, 'bills/confform.html', {'quoted_order' : quoted_order, 
                 #'quoted_item' : quoted_item, 'total_cost' : total_cost, 'id' : i_d,'form':form})
      

