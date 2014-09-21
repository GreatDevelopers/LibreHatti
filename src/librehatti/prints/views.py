#from django.http import HttpResponse
#from useraccounts.models import *
#from helper import *
from django import forms
from django.shortcuts import *
from librehatti.catalog.models import *
from django.db.models import Sum, Count
import simplejson
from forms import LabReportForm
from useraccounts.models import AdminOrganisations
from useraccounts.models import Customer
from useraccounts.models import Address
from librehatti.prints.helper import num2eng
from librehatti.voucher.models import CalculateDistribution
from librehatti.voucher.models import VoucherId
from librehatti.suspense.models import SuspenseOrder

def lab_report(request):
    """
    It generates the report which lists all the orders for the test 
    selected and the in the entered Time Span.
    """
    category = request.GET['sub_category']
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    purchase_item = PurchasedItem.objects.filter(purchase_order__date_time__range
        =(start_date,end_date),item__category=category).values(
        'purchase_order_id','purchase_order__date_time',
        'purchase_order__buyer_id__username',
        'purchase_order__buyer_id__customer__title',
        'purchase_order__buyer_id__customer__company','price',
        'purchase_order__buyer_id__customer__is_org')
    category_name = Category.objects.values('name').filter(id=category)
    
    total = PurchasedItem.objects.filter(purchase_order__date_time__range 
        = (start_date,end_date),item__category=category).\
        aggregate(Sum('price')).get('price__sum', 0.00)
    
    return render(request, 'prints/lab_reports.html', { 'purchase_item':
                   purchase_item,'start_date':start_date,'end_date':end_date,
                  'total_cost':total,'category_name':category_name})

def show_form(request):
    """
    This view is to show the form for Lab Report.
    """
    if request.method == 'POST':
        form = LabReportForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
         form = LabReportForm()
    return render(request, 'prints/show_form.html', {
              'form':form
    })
    
def filter_sub_category(request):
    """
    This view filters the sub_category according to the parent_category.
    """
    parent_category = request.GET['parent_id']
    sub_categories = Category.objects.filter(parent=parent_category)
    sub_category_dict = {}
    for sub_category in sub_categories:
        sub_category_dict[sub_category.id] = sub_category.name
    return HttpResponse(simplejson.dumps(sub_category_dict))

def bill(request):   
    """
    It generates a Bill for the user which lists all the items, 
    their quantity , subtotal and then adds it to the surcharges
    and generates the Grand total.
    """
    id = request.GET['order_id']
    purchase_order = PurchaseOrder.objects.filter(id = id)
    taxes_applied = TaxesApplied.objects.\
    filter(purchase_order=purchase_order).values('surcharge','tax')
    taxes_applied_obj = TaxesApplied.objects.\
    filter(purchase_order = purchase_order).aggregate(Count('id'))
    surcharge = Surcharge.objects.values('id','tax_name','value')
    bill = Bill.objects.values('total_cost','grand_total','delivery_charges').\
    get(purchase_order=id)
    total_cost = bill['total_cost']
    grand_total = bill['grand_total']
    delivery_charges = bill['delivery_charges']
    purchase_order_obj = PurchaseOrder.\
    objects.values('buyer','reference','delivery_address','organisation',\
    'date_time','total_discount').get(id = id)
    total_discount = purchase_order_obj['total_discount']
    taxes_applied_obj = TaxesApplied.objects.\
    filter(purchase_order = purchase_order).aggregate(Count('id'))
    suspense_order = SuspenseOrder.objects.filter(purchase_order = id)
    if suspense_order:
        if total_discount == 0:
            tax_count = taxes_applied_obj['id__count'] + 3
        else:
            tax_count = taxes_applied_obj['id__count'] + 4
    else:
        if total_discount == 0:
            tax_count = taxes_applied_obj['id__count'] + 2
        else:
            tax_count = taxes_applied_obj['id__count'] + 3
    d_address_id = purchase_order_obj['delivery_address']
    buyer = purchase_order_obj['buyer']
    organisation_id = purchase_order_obj['organisation']
    date = purchase_order_obj['date_time']
    address = Address.objects.\
    values('street_address','city','pin','province').get(id = d_address_id)
    customer_obj = Customer.objects.values('company').get(user = buyer)
    admin_organisations = AdminOrganisations.objects.values('pan_no','stc_no').\
    get(id = organisation_id)
    voucherid = VoucherId.objects.values('purchased_item__item__category__name',\
    'purchased_item__item__category','voucher_no', 'session').\
    filter(purchase_order=purchase_order).distinct().\
    order_by('purchased_item__item__category')
    voucherid_obj = VoucherId.objects.values('purchased_item__item__name',\
    'purchased_item__item__category', 'purchased_item__qty',\
    'purchased_item__item__price_per_unit').filter(purchase_order=purchase_order).\
    order_by('purchased_item__item__category')
    calculatedistribution = CalculateDistribution.objects.\
    values('voucher_no','total','session').all()
    header = HeaderOfBills.objects.values('header').order_by('-id')[0]
    return render(request, 'prints/bill.html', {'stc_no' : admin_organisations,\
        'pan_no' : admin_organisations,'ref':purchase_order_obj , 'date':date,\
        'purchase_order':purchase_order, 'purchased_item': voucherid,\
        'total_cost': total_cost ,'grand_cost': grand_total ,\
        'taxes_applied': taxes_applied ,'surcharge': surcharge,\
        'buyer': buyer, 'buyer_name': customer_obj, 'site': address,
        'delivery_charges':delivery_charges, 'total_discount':total_discount,\
        'tax_count':tax_count, 'values':voucherid_obj,\
        'cost':calculatedistribution,'header':header})


def receipt(request):
    """
    It generates a Receipt.
    """
    id = request.GET['order_id']
    bill = Bill.objects.values('amount_received').get(purchase_order = id)
    purchase_order = PurchaseOrder.objects.values('buyer','date_time',\
    'delivery_address_id','mode_of_payment__method').get(id = id)
    date = purchase_order['date_time'].date()
    total_in_words = num2eng(bill['amount_received'])
    address = Address.objects.\
    values('street_address','city','pin','province').\
    get(id = purchase_order['delivery_address_id'])
    customer_obj = Customer.objects.values('company').get(user = purchase_order['buyer'])
    purchased_item = PurchasedItem.objects.values('item__category__name').filter(purchase_order = id)
    header = HeaderOfBills.objects.values('header').order_by('-id')[0]
    return render(request, 'prints/receipt.html', {'receiptno': id,\
        'date': date, 'cost':bill, 'amount':total_in_words, 'address':address,\
        'method': purchase_order, 'buyer':customer_obj, 'material':purchased_item, 'header':header})
