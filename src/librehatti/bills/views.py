from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import Category
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import ModeOfPayment
from librehatti.catalog.models import Product
from librehatti.catalog.models import HeaderFooter
from librehatti.bills.models import QuotedTaxesApplied
from librehatti.bills.models import QuotedOrder
from librehatti.bills.models import QuotedItem
from librehatti.suspense.models import QuotedSuspenseOrder
from django.contrib.auth.models import User
import useraccounts
from django.db.models import Sum
from librehatti.bills.forms import *
from django.db.models import Max
import simplejson
from django.contrib.auth.decorators import login_required
from librehatti.bills.forms import ItemSelectForm
from django.core.urlresolvers import reverse

@login_required
def confirm(request, client_id):
    quoted_order = QuotedOrder.objects.get(pk=int(client_id))
    quoted_item = QuotedItem.objects.filter(quote_order_id=int(client_id))
    payment = ModeOfPayment.objects.all()
    items = Product.objects.all()
    i_d = quoted_order.buyer_id_id
    return render(request, 'bills/confform.html',{'quoted_order':quoted_order, 
                 'quoted_item' : quoted_item,'id':i_d,'payment':payment,'items':items})

@login_required
def final(request,name):
    if request.method == 'POST':
        form = ConfirmForm(request.POST)
        header = HeaderFooter.objects.values('header').get(is_active=True)
        if form.is_valid():
            cd = form.cleaned_data
            qty1 = request.POST ['quote_qty']
            item1 = request.POST ['quote_item']
            total_cost = PurchasedItem.objects.filter(quote_order_id=  
                         int(client_id)).aggregate(Sum('quote_price')).get('price__sum',
                         0.00)
            header = HeaderFooter.objects.values('header').get(is_active=True)
            return render(request,'bills/confirm_bill.html',
                         {'total_cost':total_cost, 'form':form , 'header':header})
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
                          'id' : i_d,'form':form, 'header':header})
	     
      
@login_required
def proforma(request):
    """
    This function lists all those customers who have added Quote
    Order. The user has the option to either generate proforma or 
    confirm it. 
    """
    QuotedOrder_list = QuotedOrder.objects.all()
    return render(request, 'bills/quote.html', 
                 {'QuotedOrder_list' : QuotedOrder_list})


@login_required
def gen_proforma(request, client_id):
    """
    It generates the Proforma Bill when the user clicks Generate 
    Proforma Button. The bill will display the item name, quantity
    and the total.
    """
    quoted_order=QuotedOrder.objects.get(buyer_id_id=client_id)
    quoted_item = QuotedItem.objects.filter(quote_order_id=
                  client_id).values_list('item__name',
                'item__category__name', 'item__price_per_unit', 'qty',
                'price')
                	
    total = QuotedItem.objects.filter(quote_order_id=client_id).aggregate(Sum(
            'price')).get('price__sum', 0.00)
    header = HeaderFooter.objects.values('header').get(is_active=True)
    return render(request, 'bills/proforma_bill.html',{ 'quoted_order':quoted_order,
                 'quoted_item' : quoted_item, 'total_cost': total, 'header':header })

@login_required
def quote_table(request,order_id):
    """
    Generates table with quoted order details.
    """
    order = QuotedOrder.objects.filter(id = order_id)
    return render(request, 'bills/table.html', {'order':order})

@login_required
def generate_bill(request):
    """
    Generates bill for the corresponding quoted order.
    """
    order = request.GET['id']
    quote_order = QuotedOrder.objects.get(id = order)
    quote_item = QuotedItem.objects.filter(quote_order_id = order).values(
    'item__name', 'qty','item__price_per_unit','price') 
    total = QuotedItem.objects.filter(quote_order_id=order).aggregate(Sum(
    'price')).get('price__sum', 0.00)
    header = HeaderFooter.objects.values('header').get(is_active=True)
    return render(request, 'bills/quote_bill.html', { 'STC_No' :'1','PAN_No' :'12', 'L_No':
    '123', 'purchase_order':quote_order, 'purchased_item' : 
     quote_item, 'total_cost': total, 'header':header})


"""
This view calculate taxes on quoted order, bill data
and save those values in database.
"""
@login_required
def quoted_bill_cal(request):
    old_post = request.session.get('old_post')
    quoted_order_id = request.session.get('quoted_order_id')
    quoted_order = QuotedOrder.objects.get(id=quoted_order_id)
    quoted_order_obj = QuotedOrder.objects.values('total_discount','tds').\
    get(id=quoted_order_id)
    quoted_item = QuotedItem.objects.\
    filter(quoted_order=quoted_order_id).aggregate(Sum('price'))
    total = quoted_item['price__sum']
    price_total = total - quoted_order_obj['total_discount']
    surcharge = Surcharge.objects.values('id','value','taxes_included')
    delivery_rate = Surcharge.objects.values('value').filter(tax_name = 'Transportation')
    distance = QuotedSuspenseOrder.objects.filter(quoted_order = quoted_order_id).\
        aggregate(Sum('distance_estimated'))
    if distance['distance_estimated__sum']:
        delivery_charges = int(distance['distance_estimated__sum'])*\
            delivery_rate[0]['value']

    else:
        delivery_charges = 0

    for value in surcharge:
        surcharge_id = value['id']
        surcharge_value = value['value']
        surcharge_tax = value['taxes_included']
        if surcharge_tax == 1:
            taxes = (price_total * surcharge_value)/100
            surcharge_obj = Surcharge.objects.get(id=surcharge_id)
            taxes_applied = QuotedTaxesApplied(quoted_order = quoted_order,
            surcharge = surcharge_obj, tax = taxes)
            taxes_applied.save()
    taxes_applied_obj = QuotedTaxesApplied.objects.\
    filter(quoted_order=quoted_order_id).aggregate(Sum('tax'))
    tax_total = taxes_applied_obj['tax__sum']
    grand_total = price_total + tax_total + delivery_charges
    amount_received = grand_total - quoted_order_obj['tds']
    bill = QuotedBill(quoted_order = quoted_order, total_cost = price_total,
    total_tax = tax_total, grand_total = grand_total,
    delivery_charges = delivery_charges, amount_received = amount_received)
    bill.save()
    request.session['old_post'] = old_post
    request.session['quoted_order_id'] = quoted_order_id
    return HttpResponseRedirect(reverse("librehatti.bills.views.quoted_order_added_success"))


@login_required
def quoted_order_added_success(request):
    quoted_order_id = request.session.get('quoted_order_id')
    details = QuotedOrder.objects.values('buyer__first_name','buyer__last_name'
        ,'buyer__customer__address__street_address','buyer__customer__title',
        'buyer__customer__address__city','mode_of_payment__method',
        'cheque_dd_number','cheque_dd_date').filter(id=quoted_order_id)[0]
    return render(request,'bills/quoted_success.html',{'details': details,
        'quoted_order_id':quoted_order_id})