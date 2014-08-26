from django.shortcuts import render
from django.http import HttpResponse
from librehatti.catalog.models import PurchaseOrder, PurchasedItem
from librehatti.bills.models import *
from django.contrib.auth.models import User
import useraccounts
from django.db.models import Sum
from librehatti.bills.forms import *
from django.db.models import Max


def confirm(request, client_id):
    quoted_order = QuotedOrder.objects.get(pk=int(client_id))
    quoted_item = QuotedItem.objects.filter(quote_order_id=
                  int(client_id)).values('quote_item__name','quote_qty',
                  'quote_price')
    form = ConfirmForm(initial={'quote_item':'quote_item','quote_qty':'quote_qty'})
    i_d = quoted_order.quote_buyer_id_id
    return render(request, 'bills/confform.html',{'quoted_order':quoted_order, 
                 'quoted_item' : quoted_item,'id':i_d,'form':form})

def final(request,name):
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            qty1 = request.POST ['quote_qty']
            item1 = request.POST ['quote_item']
            total_cost = PurchasedItem.objects.filter(quote_order_id=  
                         int(client_id)).aggregate(Sum('quote_price')).get('price__sum',
                         0.00)
            return render(request,'bills/confirm_bill.html',
                         {'total_cost':total_cost, 'form':form })
        else:
    
             client_id = 1
             quoted_order = QuotedOrder.objects.get(pk=int(client_id))
             quoted_item = QuotedItem.objects.filter().values('quote_item__name',
                           'quote_qty', 'quote_price')
             
             total_cost = QuotedItem.objects.filter(quote_order_id=
                          int(client_id)).aggregate(Sum('quote_price')).get('price__sum', 
                          0.00)
             i_d = quoted_order.quote_buyer_id_id
             return render(request, 'bills/confirm_bill.html', 
                          {'quoted_order' : quoted_order, 
                          'quoted_item' : quoted_item, 'total_cost' : total_cost, 
                          'id' : i_d,'form':form})
      
def proforma(request):
    """
    This function lists all those customers who have added Quote
    Order. The user has the option to either generate proforma or 
    confirm it. 
    """
    QuotedOrder_list = QuotedOrder.objects.all()
    return render(request, 'bills/quote.html', 
                 {'QuotedOrder_list' : QuotedOrder_list})


def gen_proforma(request, client_id):
    """
    It generates the Proforma Bill when the user clicks Generate 
    Proforma Button. The bill will display the item name, quantity
    and the total.
    """
    quoted_order=QuotedOrder.objects.get(quote_buyer_id_id=client_id)
    quoted_item = QuotedItem.objects.filter(quote_order_id=
                  client_id).values_list('quote_item__name',
                'quote_item__category__name', 'quote_item__price_per_unit', 'quote_qty',
                'quote_price')
                	
    total = QuotedItem.objects.filter(quote_order_id=client_id).aggregate(Sum(
            'quote_price')).get('quote_price__sum', 0.00)
    return render(request, 'bills/proforma_bill.html',{ 'quoted_order':quoted_order,
                 'quoted_item' : quoted_item, 'total_cost': total })	 
  

