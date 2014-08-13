from django.shortcuts import render
from django.http import HttpResponse
from librehatti.catalog.models import PurchaseOrder, PurchasedItem
from librehatti.bills.models import *
from django.contrib.auth.models import User
import useraccounts
from django.db.models import Sum
from librehatti.bills.forms import *
from librehatti.prints.helper import num2eng
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
            total_cost = PurchasedItem.objects.filter(quote_order_id=int(client_id)).aggregate(Sum('price')).get('price__sum', 0.00)
            return render(request, 'bills/confirm.html', {'total_cost' : total_cost, 'form':form })
        else:
    
             client_id = 1
             quoted_order = QuotedOrder.objects.get(pk=int(client_id))
             quoted_item = QuotedItem.objects.filter().values('quote_item__name', 'quote_qty', 'quote_price')
             
             total_cost = QuotedItem.objects.filter(quote_order_id=int(client_id)).aggregate(Sum('quote_price')).get('price__sum', 0.00)
             i_d = quoted_order.quote_buyer_id_id
             return render(request, 'bills/confirm.html', {'quoted_order' : quoted_order, 
                 'quoted_item' : quoted_item, 'total_cost' : total_cost, 'id' : i_d,'form':form})
      
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
                'quote_item__category__name', 'quote_item__price', 'quote_qty',
                'quote_price')	
    total = QuotedItem.objects.filter(quote_order_id=client_id).aggregate(Sum(
            'quote_price')).get('quote_price__sum', 0.00)
    return render(request, 'bills/p_bill.html',{ 'quoted_order':quoted_order,
                 'quoted_item' : quoted_item, 'total_cost': total })	 
  


def transport(request):
    form = TransportForm1()
    temp = {'TransportForm':form}
    return render (request, 'bills/form.html',temp)


def transport_bill(request):
    if request.method == 'POST':
        form = TransportForm1(request.POST)
        if form.is_valid():
           
            if 'button1' in request.POST:
                    vehicle_id = request.POST['vehicle_id']
                    job_id = request.POST['job_id']
                    kilometer = float(request.POST['kilometer'])          
                    date = request.POST['date']
                    rate = float(request.POST['rate'])
                    total = rate*kilometer
                    obj = Transport(vehicle_id=vehicle_id, job_id=job_id, 
                           kilometer=kilometer, Date=date, rate=rate, 
                           total=total) 
                    obj.save()
                    temp = Transport.objects.filter(job_id=obj.job_id)
                    total_amount = Transport.objects.filter(job_id=obj.job_id
                           ).aggregate(Sum('total')).get('total__sum', 0.00)
                    return render(request,'bills/transport_bill.html', 
                           {'temp' : temp, 'words' : num2eng(total_amount), 
                            'total_amount' : total_amount}) 

            else:
                    vehicle_id = request.POST['vehicle_id']
                    job_id = request.POST['job_id']
                    kilometer = float(request.POST['kilometer'])
                    date = request.POST['date']
                    rate = float(request.POST['rate'])
                    total = rate * kilometer
                    obj = Transport(vehicle_id=vehicle_id, job_id=job_id, 
                                    kilometer=kilometer, Date=date, rate=rate, 
                                    total=total) 
                    obj.save()
                         
    else:
        form = TransportForm1()
    return render(request, 'bills/form.html', {'TransportForm':form})         
  
