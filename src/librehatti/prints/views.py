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
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from librehatti.bills.models import QuotedOrder
from librehatti.bills.models import QuotedBill
from librehatti.bills.models import QuotedTaxesApplied
from librehatti.bills.models import QuotedItem
from librehatti.bills.models import QuoteNote

from librehatti.suspense.models import QuotedSuspenseOrder

@login_required
def lab_report(request):
    """
    It generates the report which lists all the orders for the test
    selected and the in the entered Time Span.
    """
    category = request.GET['sub_category']
    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    if start_date > end_date:
        error_type = "Date range error"
        error = "Start date cannot be greater than end date"
        temp = {'type': error_type, 'message':error}
        return render(request,'error_page.html',temp)

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

@login_required
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

@login_required
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

@login_required
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
    objects.values('buyer','buyer__first_name','buyer__last_name','reference','delivery_address','organisation',\
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
    buyer = purchase_order_obj['buyer']
    address = Customer.objects.values('address__street_address',\
    'address__city', 'address__pin', 'address__province').get(user = buyer)
    organisation_id = purchase_order_obj['organisation']
    date = purchase_order_obj['date_time']
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
    header = HeaderFooter.objects.values('header').get(is_active=True)
    footer = HeaderFooter.objects.values('footer').get(is_active=True)
    return render(request, 'prints/bill.html', {'stc_no' : admin_organisations,\
        'pan_no' : admin_organisations,'id':id,'ref':purchase_order_obj , 'date':date,\
        'purchase_order':purchase_order, 'purchased_item': voucherid,'address':address,\
        'total_cost': total_cost ,'grand_cost': grand_total ,\
        'taxes_applied': taxes_applied ,'surcharge': surcharge,\
        'buyer': purchase_order_obj, 'buyer_name': customer_obj, 'site': purchase_order_obj,
        'delivery_charges':delivery_charges, 'total_discount':total_discount,\
        'tax_count':tax_count, 'values':voucherid_obj,\
        'cost':calculatedistribution,'header':header,'footer': footer})


@login_required
def tax(request):
    """
    It generates a tax details bill for the user which lists all the taxes,
    their applied tax value , calculated tax and generates the total of the
    applied taxes.
    """
    id = request.GET['order_id']
    taxes_applied = TaxesApplied.objects.values('surcharge__tax_name','surcharge__value',\
        'tax','purchase_order__date_time').filter(purchase_order=id)
    bill = Bill.objects.values('total_cost','total_tax',\
        'purchase_order__date_time').get(purchase_order=id)
    grand_total = bill['total_cost'] + bill['total_tax']
    header = HeaderFooter.objects.values('header').get(is_active=True)
    footer = HeaderFooter.objects.values('footer').get(is_active=True)
    return render(request, 'prints/tax.html',{'id':id,'details':taxes_applied,\
        'bill':bill,'grand_total':grand_total,\
        'header':header,'footer':footer})


@login_required
def receipt(request):
    """
    It generates a Receipt.
    """
    id = request.GET['order_id']
    bill = Bill.objects.values('amount_received').get(purchase_order = id)
    purchase_order = PurchaseOrder.objects.values('buyer','date_time',\
    'delivery_address','mode_of_payment__method').get(id = id)
    date = purchase_order['date_time'].date()
    total_in_words = num2eng(bill['amount_received'])
    customer_obj = Customer.objects.values('company').get(user = purchase_order['buyer'])
    address = Customer.objects.values('address__street_address',\
    'address__city', 'address__pin', 'address__province').get(user = purchase_order['buyer'])
    purchased_item = PurchasedItem.objects.values('item__category__name').filter(purchase_order = id).distinct()
    header = HeaderFooter.objects.values('header').get(is_active=True)
    return render(request, 'prints/receipt.html', {'receiptno': id,\
        'date': date, 'cost':bill, 'amount':total_in_words, 'address':address,\
        'method': purchase_order, 'buyer':customer_obj, 'material':purchased_item, 'header':header})


@login_required
def quoted_bill(request):
    quoted_order_id = request.GET['quoted_order_id']
    quoted_order = QuotedOrder.objects.filter(id = quoted_order_id)
    quoted_item = QuotedItem.objects.filter(quoted_order=quoted_order_id).\
    values('item__category__name',\
    'item__category').\
    order_by('item__category').distinct()
    quoted_item_odj = QuotedItem.objects.filter(quoted_order=quoted_order_id).\
    values('item__name',\
    'item__category', 'qty',\
    'item__price_per_unit').order_by('item__category')
    cost = QuotedItem.objects.filter(quoted_order=quoted_order_id).\
    values('price','item__category','item__name').order_by('item__category')
    taxes_applied = QuotedTaxesApplied.objects.\
    filter(quoted_order=quoted_order).values('surcharge','tax')
    taxes_applied_obj = QuotedTaxesApplied.objects.\
    filter(quoted_order = quoted_order).aggregate(Count('id'))
    surcharge = Surcharge.objects.values('id','tax_name','value')
    bill = QuotedBill.objects.values('total_cost','grand_total','delivery_charges').\
    get(quoted_order=quoted_order_id)
    total_cost = bill['total_cost']
    grand_total = bill['grand_total']
    delivery_charges = bill['delivery_charges']
    quoted_order_obj = QuotedOrder.\
    objects.values('buyer','buyer__first_name','buyer__last_name','reference','delivery_address','organisation',\
    'date_time','total_discount').get(id = quoted_order_id)
    total_discount = quoted_order_obj['total_discount']
    taxes_applied_obj = QuotedTaxesApplied.objects.\
    filter(quoted_order = quoted_order).aggregate(Count('id'))
    suspense_order = QuotedSuspenseOrder.objects.filter(quoted_order = quoted_order_id)
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
    buyer = quoted_order_obj['buyer']
    address = Customer.objects.values('address__street_address',\
    'address__city', 'address__pin', 'address__province').get(user = buyer)
    organisation_id = quoted_order_obj['organisation']
    date = quoted_order_obj['date_time']
    customer_obj = Customer.objects.values('company').get(user = buyer)
    admin_organisations = AdminOrganisations.objects.values('pan_no','stc_no').\
    get(id = organisation_id)
    header = HeaderFooter.objects.values('header').get(is_active=True)
    footer = HeaderFooter.objects.values('footer').get(is_active=True)
    note = QuoteNote.objects.values('note').get(is_active=True)
    return render(request, 'prints/quote_bill.html', {'stc_no' : admin_organisations,\
        'pan_no' : admin_organisations,'id':id,'ref':quoted_order_obj , 'date':date,\
        'quoted_order':quoted_order, 'address':address,\
        'total_cost': total_cost ,'grand_cost': grand_total ,\
        'taxes_applied': taxes_applied ,'surcharge': surcharge,\
        'buyer': quoted_order_obj, 'buyer_name': customer_obj, 'site': quoted_order_obj,
        'delivery_charges':delivery_charges, 'total_discount':total_discount,\
        'tax_count':tax_count,'quoted_item':quoted_item,'values':quoted_item_odj,\
        'cost':cost,'header':header,'footer': footer,'note':note})