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


def list_quoted(request):
    quoted = QuotedItem.objects.values('quote_order__id',
            'quote_order__quote_buyer_id__username').filter(confirm_status = 0)
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
        quoted_item = objects.filter.quote(order_id_quote = 
                      order_QuotedItem_id).values('quote_item__name', 
                      'quote_qty','quote_discount')
        client_id = QuotedOrder.objects.values("quote_buyer_id__id").filter(
                    id = quote_order_id)
        form = ConfirmForm(initial={'quote_item':'item1', 'qty1':'quote_qty'})
        return render(request, 'bills/confform.html', {'form':form,
                     'client_id':client_id, 'quoted_item' : quoted_item})


def proforma(request):
    QuotedOrder_list = PurchaseOrder.objects.all()
    return render(request, 'bills/quote.html', 
                 {'QuotedOrder_list' : QuotedOrder_list})


def gen_proforma(request, client_id):
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
    form = transportform()
    temp = {'transportform':form}
    return render (request, 'bills/form.html',temp)


def transport_bill(request):
    if request.method == 'POST':
        form = transportform(request.POST)
        c = {}
        if form.is_valid():
            if 'button1' in request.POST:
                    vehicle_id = request.POST['vehicle_id']
                    job_id = request.POST['job_id']
                    kilometer = request.POST['kilometer']          
                    date = request.POST['date']
                    rate = float(request.POST['rate'])
                    total = rate*float(kilometer)
                    obj = Transport(vehicle_id=vehicle_id, job_id=job_id, 
                                    kilometer=kilometer, Date=date, rate=rate, 
                                    total=total) 
                    obj.save()
                    temp = Transport.objects.filter(job_id=obj.job_id)
                    total_amount = Transport.objects.filter(job_id=obj.job_id
                           ).aggregate(Sum('total')).get('total__sum', 0.00)
                    return render(request,'bills/transport_bill.html', 
                           {'temp' : temp, 'words' : num2eng(int(total)), 
                            'total_amount' : total_amount}) 
            if 'button2' in request.POST:          
                    form1 = transportform()
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
        form = transportform()
    return render(request, 'bills/form.html', {'transportform':form})         
  
  
