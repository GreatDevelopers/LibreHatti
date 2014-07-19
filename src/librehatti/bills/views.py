from django.shortcuts import render
from django.http import HttpResponse
from librehatti.catalog.models import PurchaseOrder, PurchasedItem
from librehatti.bills.models import *
from django.contrib.auth.models import User
import useraccounts
from django.db.models import Sum
from librehatti.bills.forms import ConfirmForm


def list_quoted(request):
    quoted_order = QuotedOrder.objects.get(pk=1)
    quoted_item = QuotedItem.objects.filter(quote_order_id=1).values('quote_item__name', 'quote_qty')
    i_d = quoted_order.quote_buyer_id_id
    form = ConfirmForm(initial={'quote_item':'item1', 'qty1':'quote_qty'})
    return render(request, 'bills/confform.html', {'quoted_order' : quoted_order,'form':form,
                 'quoted_item' : quoted_item,  'id' : i_d})



def confirm(request):
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponse('helo')
            quote_qty = request.POST ["quote_qty"]
            quote_item = request.POST ["quote_item"]
            #return HttpResponse('quote_qty')
            #obj = PurchasedItem(qty=quote_qty)
            #obj.item= PurchasedItem.objects.get(item__name=quote_item)
            #obj.purchase_order= PurchaseOrder.objects.get(id=client_id)
            #obj.save()
            #quoted_item = PurchasedItem.objects.filter(client_id=buyer_id).values( 'item__name','qty')
            
            return render(request, 'bills/bills.html',{'form':form})

    else:
             client_id = 1
             quoted_order = QuotedOrder.objects.get(pk=int(client_id))
             quoted_item = QuotedItem.objects.filter(quote_order_id=int(client_id)).values_list('quote_item__name', 'quote_qty', 'quote_price')
             total_cost = QuotedItem.objects.filter(quote_order_id=int(client_id)).aggregate(Sum('quote_price')).get('price__sum', 0.00)
             i_d = quoted_order.quote_buyer_id_id
             form = ConfirmForm()
             return render(request, 'bills/bills.html', {'quoted_order' : quoted_order, 
                 'quoted_item' : quoted_item, 'total_cost' : total_cost, 'id' : i_d,'form':form})

def proforma(request):
    QuotedOrder_list = PurchaseOrder.objects.all()
    return render(request, 'bills/quote.html', 
                 {'QuotedOrder_list' : QuotedOrder_list})


def gen_proforma(request, client_id):
    quoted_order=QuotedOrder.objects.get(quote_buyer_id_id=client_id)
    quoted_item = QuotedItem.objects.filter(quote_order_id=
                  client_id).values_list('quote_item__name',
                'quote_item__category__name', 'quote_item__price_per_unit', 'quote_qty',
                'quote_price')	
    total = QuotedItem.objects.filter(quote_order_id=client_id).aggregate(Sum(
            'quote_price')).get('quote_price__sum', 0.00)
    return render(request, 'bills/p_bill.html',{ 'quoted_order':quoted_order,
                 'quoted_item' : quoted_item, 'total_cost': total })	 
  
