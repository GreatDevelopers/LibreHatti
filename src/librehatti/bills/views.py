from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import ModeOfPayment
from librehatti.catalog.models import Product
from librehatti.catalog.models import HeaderFooter
from librehatti.bills.models import *
from django.contrib.auth.models import User
import useraccounts
from django.db.models import Sum
from librehatti.bills.forms import *
from django.db.models import Max
import simplejson
from django.contrib.auth.decorators import login_required

def confirm(request, client_id):
    quoted_order = QuotedOrder.objects.get(pk=int(client_id))
    quoted_item = QuotedItem.objects.filter(quote_order_id=int(client_id))
    payment = ModeOfPayment.objects.all()
    items = Product.objects.all()
    i_d = quoted_order.buyer_id_id
    return render(request, 'bills/confform.html',{'quoted_order':quoted_order, 
                 'quoted_item' : quoted_item,'id':i_d,'payment':payment,'items':items})

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

def quote_table(request,order_id):
    """
    Generates table with quoted order details.
    """
    order = QuotedOrder.objects.filter(id = order_id)
    return render(request, 'bills/table.html', {'order':order})

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


def select_sub_category(request):
    """
    This view allows filtering of sub category according to parent category of 
    item.
    """
    parent_category = request.GET['cat_id']
    sub_categories = Category.objects.filter(parent=parent_category)
    sub_category_dict = {}
    for sub_category in sub_categories:
        sub_category_dict[sub_category.id] = sub_category.name
    return HttpResponse(simplejson.dumps(sub_category_dict))

def select_item(request):
    """
    This view allows filtering of item according to sub category of item.
    """
    cat_id = request.GET['cat_id']
    products = Product.objects.filter(category = cat_id)
    product_dict = {}
    for product in products:
        product_dict[product.id] = product.name
    return HttpResponse(simplejson.dumps(product_dict))  

def bill_cal(request):
    """
    This view calculate taxes on quoted order, bill data
    and save those values in database.
    """
    old_post = request.session.get('old_post')
    quote_order_id = request.session.get('quote_order_id')
    quote_order = QuotedOrder.objects.get(id=quote_order_id)
    quote_item = QuotedItem.objects.\
    filter(quote_order=quote_order_id).aggregate(Sum('price'))
    price_total = quote_item['price__sum']
    surcharge = Surcharge.objects.values('id','value')
    for value in surcharge:
        surcharge_id = value['id']
        surcharge_value = value['value']
        taxes = (price_total * surcharge_value)/100
        surcharge_obj = Surcharge.objects.get(id=surcharge_id)
        taxes_applied = QuoteTaxesApplied(quote_order = quote_order,
        surcharge = surcharge_obj, tax = taxes)
        taxes_applied.save()
    taxes_applied_obj = QuoteTaxesApplied.objects.\
    filter(quote_order=quote_order_id).aggregate(Sum('tax'))
    tax_total = taxes_applied_obj['tax__sum']
    grand_total = price_total + tax_total
    bill = QuotedBill(quote_order = quote_order, total_cost = price_total,
    total_tax = tax_total, grand_total = grand_total)
    bill.save()
    request.session['old_post'] = old_post
    request.session['quote_order_id'] = quote_order_id
    return HttpResponseRedirect('/suspense/quoted_add_distance/')          



		 
  

