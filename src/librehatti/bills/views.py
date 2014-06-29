
from django.shortcuts import render
from librehatti.catalog.models import *
from librehatti.bills.models import *
from django.contrib.auth.models import User
import useraccounts
from django.db.models import Sum

def proforma(request):

    QuotedOrder_list = PurchaseOrder.objects.all()
   
    return render(request, 'bills/quote.html', 
                 {'QuotedOrder_list' : QuotedOrder_list})


def gen_proforma(request, client_id):
    
    quoted_order=QuotedOrder.objects.get(quote_buyer_id_id=client_id)
    quoted_item = QuotedItem.objects.filter(quote_order_id=client_id).values_list('quote_item__name' ,
		           'quote_item__category__name','quote_item__price','quote_qty' , 'quote_price')	
    total = QuotedItem.objects.filter(quote_order_id=client_id).aggregate(Sum('quote_price')).get('quote_price__sum', 0.00)
    return render(request, 'bills/p_bill.html',{ 'quoted_order':quoted_order,'quoted_item' : quoted_item , 'total_cost': total} )	 
  