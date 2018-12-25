#from django.http import HttpResponse
#from useraccounts.models import *
#from helper import *
from django import forms

from django.shortcuts import *

from django.contrib.auth.decorators import login_required

from django.urls import reverse

from librehatti.catalog.models import *
from librehatti.catalog.request_change import request_notify

from django.db.models import Sum, Count

import simplejson

from useraccounts.models import AdminOrganisations
from useraccounts.models import Customer
from useraccounts.models import Address

from librehatti.prints.helper import num2eng

from librehatti.voucher.models import CalculateDistribution
from librehatti.voucher.models import VoucherId, FinancialSession

from librehatti.suspense.models import SuspenseOrder
from librehatti.suspense.models import QuotedSuspenseOrder

from librehatti.bills.models import QuotedOrder
from librehatti.bills.models import QuotedBill
from librehatti.bills.models import QuotedTaxesApplied
from librehatti.bills.models import QuotedItem
from librehatti.bills.models import NoteLine
from librehatti.bills.models import QuotedOrderNote
from librehatti.bills.models import QuotedOrderofSession

from librehatti.config import _ACCOUNT_HOLDER
from librehatti.config import _NAME_OF_BANK
from librehatti.config import _BRANCH
from librehatti.config import _ONLINE_ACCOUNT
from librehatti.config import _IFSC_CODE
from librehatti.config import _YOUR_LETTER_No

from django.db.models import Max

@login_required
def bill(request):
    """
    It generates a bill for the user which lists all the items,
    their quantity , subtotal and then adds it to the surcharges
    and generates the Grand total.
    Argument:Http Request
    Return:Render Bill
    """
    id = request.GET['order_id']
    purchase_order = PurchaseOrder.objects.filter(id=id)
    purchased_item = PurchasedItem.objects.filter(\
        purchase_order=purchase_order).values('item__category__name',\
        'item__category','item__category__parent__name','item__category__unit',\
        'item__category__unit__unit').\
        order_by('item__category').distinct()
    purchased_item_obj = PurchasedItem.objects.filter(\
        purchase_order=purchase_order).values('item__name', 'item__category',\
        'qty', 'price_per_unit').order_by('item__category')
    cost = PurchasedItem.objects.filter(purchase_order=purchase_order).\
    values('price', 'item__category', 'item__name',\
        'item__category__parent__name').order_by('item__category')
    bill_obj = Bill.objects.values('delivery_charges').get(purchase_order=id)
    bill_values = []
    field_check = 1
    for category in purchased_item:
        flag1 = 1
        list = []
        list.append(category['item__category__name'])
        item_names = []
        for item in purchased_item_obj:
            if category['item__category'] == item['item__category']:
                if flag1 == 1:
                    item_names.append(':')
                    item_names.append(item['item__name'])
                    flag1 = 0
                else:
                    item_names.append(',')
                    item_names.append(item['item__name'])
        flag1 = 1
        item_qty = []
        for qty in purchased_item_obj:
            if category['item__category'] == qty['item__category']:
                if flag1 == 1:
                    item_qty.append(qty['qty'])
                    flag1 = 0
                else:
                    item_qty.append(',')
                    item_qty.append(qty['qty'])
        if category['item__category__unit']:
            item_qty.append(category['item__category__unit__unit'])
        else:
            item_qty.append('no_unit')
        flag1 = 1
        price_unit = []
        for price_per in purchased_item_obj:
            if category['item__category'] == price_per['item__category']:
                if flag1 == 1:
                    price_unit.append(price_per['price_per_unit'])
                    flag1 = 0
                else:
                    price_unit.append(',')
                    price_unit.append(price_per['price_per_unit'])
        total=0
        for itemcost in cost:
            if category['item__category'] == itemcost['item__category']:
                total = total + itemcost['price']
        list.append(item_names)
        list.append(item_qty)
        list.append(price_unit)
        list.append(total)
        bill_values.append(list)
    taxes_applied = TaxesApplied.objects.\
    filter(purchase_order=purchase_order).values('surcharge', 'tax',
        'surcharge_name', 'surcharge_value')
    taxes_applied_obj = TaxesApplied.objects.\
    filter(purchase_order=purchase_order).aggregate(Count('id'))
    bill = Bill.objects.values('total_cost', 'totalplusdelivery',\
        'grand_total', 'delivery_charges').get(purchase_order=id)
    total_cost = bill['total_cost']
    totalplusdelivery = bill['totalplusdelivery']
    grand_total = bill['grand_total']
    delivery_charges = bill['delivery_charges']
    purchase_order_obj = PurchaseOrder.objects.values('buyer',\
        'buyer__first_name', 'buyer__last_name', 'reference','reference_date',\
        'delivery_address', 'organisation', 'date_time', 'total_discount',\
        'buyer__customer__title').get(id = id)
    total_discount = purchase_order_obj['total_discount']
    taxes_applied_obj = TaxesApplied.objects.\
    filter(purchase_order=purchase_order).aggregate(Count('id'))
    suspense_order = SuspenseOrder.objects.values('distance_estimated').\
    filter(purchase_order=id)
    total_distance = 0
    if suspense_order:
        for distance in suspense_order:
            total_distance = total_distance + distance['distance_estimated']
        if total_distance == 0:
            if total_discount == 0:
                tax_count = taxes_applied_obj['id__count'] + 2
            else:
                tax_count = taxes_applied_obj['id__count'] + 3
        else:
            if total_discount == 0:
                tax_count = taxes_applied_obj['id__count'] + 4
            else:
                tax_count = taxes_applied_obj['id__count'] + 5
    else:
        if total_discount == 0:
            tax_count = taxes_applied_obj['id__count'] + 2
        else:
            tax_count = taxes_applied_obj['id__count'] + 3
    if taxes_applied_obj['id__count'] == 0:
        tax_count = tax_count + 1
    buyer = purchase_order_obj['buyer']
    address = Customer.objects.values('address__street_address',\
    'address__district', 'address__pin', 'address__province').get(user=buyer)
    organisation_id = purchase_order_obj['organisation']
    date = purchase_order_obj['date_time']
    customer_obj = Customer.objects.values('company').get(user=buyer)
    customer_gst_details = Customer.objects.values('gst_in', 'state', 'state_code').get(user=buyer)
    admin_organisations = AdminOrganisations.objects.values('pan_no',\
        'stc_no', 'gst_in', 'state', 'state_code').get(id=organisation_id)
    voucherid = VoucherId.objects.values('purchase_order_of_session').\
    filter(purchase_order=id)[0]
    total_in_words=num2eng(grand_total)
    ref_letter = _YOUR_LETTER_No
    header = HeaderFooter.objects.values('header').get(is_active=True)
    footer = HeaderFooter.objects.values('footer').get(is_active=True)
    return render(request, 'prints/bill.html', {\
        'admin_org' : admin_organisations,\
        'id':voucherid['purchase_order_of_session'], 'ref':purchase_order_obj,\
        'date':date, 'purchase_order':purchase_order, 'address':address,\
        'total_cost':total_cost, 'grand_cost':grand_total,\
        'taxes_applied':taxes_applied, 'customer_gst_details':customer_gst_details,\
        'buyer':purchase_order_obj, 'buyer_name':customer_obj,\
        'site':purchase_order_obj, 'delivery_charges':delivery_charges,\
        'total_discount':total_discount, 'tax_count':tax_count,\
        'bill_values':bill_values, 'header':header, 'footer': footer,\
        'totalplusdelivery':totalplusdelivery,\
        'total_in_words':total_in_words, 'ref_letter':ref_letter})


@login_required
def suspense_bill(request):
    """
    It generates a Suspense Bill for the user which lists all the items,
    their quantity , subtotal and then adds it to the surcharges
    and generates the Grand total.
    Argument:Http Request
    Return:Render Suspense Bill
    """
    id = request.GET['order_id']
    voucherid = VoucherId.objects.filter(purchase_order=id).\
    values('voucher_no', 'purchased_item__item__category', 'session').distinct()
    suspenseorder = SuspenseOrder.objects.values('voucher', 'session_id',\
        'distance_estimated').filter(purchase_order=id)
    rate = Surcharge.objects.values('value').\
        filter(tax_name = 'Transportation')[0]
    for distance_temp in suspenseorder:
        distance = distance_temp['distance_estimated'] * rate['value']
        distance_temp['distance_estimated'] = distance
    purchased_item = PurchasedItem.objects.filter(\
        purchase_order=id).values('item__category__name',\
        'item__category','item__category__parent__name').\
        order_by('item__category').distinct()
    purchased_item_obj = PurchasedItem.objects.filter(\
        purchase_order=id).values('item__name', 'item__category',\
        'qty', 'price_per_unit').order_by('item__category')
    cost = PurchasedItem.objects.filter(purchase_order=id).\
    values('price', 'item__category', 'item__name',\
        'item__category__parent__name').order_by('item__category')
    bill = Bill.objects.values('totalplusdelivery','grand_total').get(purchase_order=id)
    bill_values = []
    field_check = 1
    for category in purchased_item:
        flag1 = 1
        list = []
        list.append(category['item__category__name'])
        item_names = []
        for item in purchased_item_obj:
            if category['item__category'] == item['item__category']:
                if flag1 == 1:
                    item_names.append(':')
                    item_names.append(item['item__name'])
                    flag1 = 0
                else:
                    item_names.append(',')
                    item_names.append(item['item__name'])
        flag1 = 1
        total=0
        for itemcost in cost:
            if category['item__category'] == itemcost['item__category']:
                total = total + itemcost['price']
        for voucher_obj in voucherid:
            if category['item__category'] == voucher_obj['purchased_item__item__category']:
                try:
                    suspense_obj = SuspenseOrder.objects.values(\
                        'distance_estimated').get(\
                        voucher=voucher_obj['voucher_no'],\
                        session_id=voucher_obj['session'])
                    total = total + suspense_obj['distance_estimated'] * rate['value']
                except:
                    pass
        list.append(item_names)
        list.append(int(total))
        bill_values.append(list)
    taxes_applied = TaxesApplied.objects.\
    filter(purchase_order=id).values('surcharge', 'tax')
    taxes_applied_obj = TaxesApplied.objects.\
    filter(purchase_order=id).aggregate(Count('id'))
    surcharge = Surcharge.objects.values('id', 'tax_name', 'value')
    totalplusdelivery = bill['totalplusdelivery']
    grand_total = bill['grand_total']
    purchase_order_obj = PurchaseOrder.objects.values('buyer',\
        'buyer__first_name', 'buyer__last_name', 'reference','reference_date',\
        'delivery_address', 'organisation', 'date_time', 'total_discount',\
        'buyer__customer__title').get(id = id)
    taxes_applied_obj = TaxesApplied.objects.\
    filter(purchase_order=id).aggregate(Count('id'))
    buyer = purchase_order_obj['buyer']
    address = Customer.objects.values('address__street_address',\
    'address__district', 'address__pin', 'address__province').get(user=buyer)
    organisation_id = purchase_order_obj['organisation']
    date = purchase_order_obj['date_time']
    customer_obj = Customer.objects.values('company').get(user=buyer)
    admin_organisations = AdminOrganisations.objects.values('pan_no',\
        'stc_no').get(id=organisation_id)
    voucherid = VoucherId.objects.values('purchase_order_of_session').\
    filter(purchase_order=id)[0]
    total_in_words=num2eng(grand_total)
    ref_letter = _YOUR_LETTER_No
    header = HeaderFooter.objects.values('header').get(is_active=True)
    footer = HeaderFooter.objects.values('footer').get(is_active=True)
    return render(request, 'prints/suspense_bill.html', {\
        'stc_no' : admin_organisations, 'pan_no' : admin_organisations,\
        'id':voucherid['purchase_order_of_session'], 'ref':purchase_order_obj,\
        'date':date, 'address':address,\
        'grand_cost':grand_total,\
        'taxes_applied':taxes_applied, 'surcharge':surcharge,\
        'buyer':purchase_order_obj, 'buyer_name':customer_obj,\
        'site':purchase_order_obj,\
        'bill_values':bill_values, 'header':header, 'footer': footer,\
        'totalplusdelivery':totalplusdelivery,\
        'total_in_words':total_in_words, 'ref_letter':ref_letter})


@login_required
def tax(request):
    """
    It generates a tax details for the user which lists all the taxes,
    their applied tax value , calculated tax and generates the total of the
    applied taxes.
    Argument:Http Request
    Return:Render Tax Details
    """
    id = request.GET['order_id']
    taxes_applied = TaxesApplied.objects.values('surcharge__tax_name',\
        'surcharge__value', 'tax', 'purchase_order__date_time',
        'surcharge_name', 'surcharge_value').\
    filter(purchase_order=id)
    bill = Bill.objects.values('totalplusdelivery','total_tax',\
        'purchase_order__date_time').get(purchase_order=id)
    grand_total = bill['totalplusdelivery'] + bill['total_tax']
    voucherid = VoucherId.objects.values('purchase_order_of_session').\
    filter(purchase_order=id)[0]
    header = HeaderFooter.objects.values('header').get(is_active=True)
    footer = HeaderFooter.objects.values('footer').get(is_active=True)
    return render(request, 'prints/tax.html',{\
        'id':voucherid['purchase_order_of_session'], 'details':taxes_applied,\
        'bill':bill, 'grand_total':grand_total, 'header':header,\
        'footer':footer})


@login_required
def receipt(request):
    """
    It generates a Receipt.
    Argument:Http Request
    Return:Render Receipt
    """
    id = request.GET['order_id']
    voucherid_temp = VoucherId.objects.values('receipt_no_of_session').filter(
        purchase_order=id)[0]
    if not voucherid_temp['receipt_no_of_session']:
        today_date = datetime.date.today()
        financialsession = FinancialSession.objects.\
        values('id','session_start_date','session_end_date')
        for value in financialsession:
            start_date = value['session_start_date']
            end_date = value['session_end_date']
            if start_date <= today_date <= end_date:
                session_id = value['id']
        max_receipt_no = VoucherId.objects.filter(session=session_id).aggregate(Max('receipt_no_of_session'))
        if max_receipt_no['receipt_no_of_session__max']:
            voucherid_obj = VoucherId.objects.values('receipt_no_of_session',
                'session', 'purchase_order__date_time').filter(
                receipt_no_of_session=max_receipt_no['receipt_no_of_session__max'],
                session_id=session_id)[0]
            voucherid_obj2 = VoucherId.objects.values('receipt_no_of_session',
                'session', 'purchase_order__date_time').filter(purchase_order=id)[0]
            if voucherid_obj['session'] == voucherid_obj2['session']:
                VoucherId.objects.filter(purchase_order=id).update(
                    receipt_no_of_session=max_receipt_no['receipt_no_of_session__max']+1,
                    receipt_date=today_date)
            else:
                VoucherId.objects.filter(purchase_order=id).update(
                    receipt_no_of_session=1,receipt_date=today_date)
        else:
            VoucherId.objects.filter(purchase_order=id).update(
                receipt_no_of_session=1,receipt_date=today_date)
    voucherid = VoucherId.objects.values('purchase_order_of_session',
        'receipt_no_of_session').\
    filter(purchase_order=id)[0]
    bill = Bill.objects.values('amount_received').get(purchase_order=id)
    purchase_order = PurchaseOrder.objects.values('buyer', 'date_time',\
    'delivery_address', 'mode_of_payment__method','mode_of_payment',\
    'cheque_dd_number', 'cheque_dd_date','buyer__customer__company').get(id=id)
    date = purchase_order['date_time']
    total_in_words = num2eng(bill['amount_received'])
    customer_obj = PurchaseOrder.objects.values('buyer',\
        'buyer__first_name', 'buyer__last_name','buyer__customer__title').\
    get(id = id)
    address = Customer.objects.values('address__street_address',\
    'address__district', 'address__pin', 'address__province').\
    get(user = purchase_order['buyer'])
    purchased_item = PurchasedItem.objects.values('item__category__name').\
    filter(purchase_order=id).distinct()
    header = HeaderFooter.objects.values('header').get(is_active=True)
    return render(request, 'prints/receipt.html', {\
        'receiptno': voucherid['receipt_no_of_session'],
        'order_no':voucherid['purchase_order_of_session'],
        'date': date, 'cost':bill, 'amount':total_in_words, 'address':address,\
        'method': purchase_order, 'buyer':customer_obj,\
        'material':purchased_item, 'header':header})


@login_required
def quoted_bill(request):
    """
    It generates a proforma bill for the user which lists all the items,
    their quantity , subtotal and then adds it to the surcharges
    and generates the Grand total.
    Argument:Http Request
    Return:Render Proforma Bill
    """
    quoted_order_id = request.GET['quoted_order_id']
    quoted_order = QuotedOrder.objects.filter(id=quoted_order_id)
    quoted_item = QuotedItem.objects.filter(quoted_order=quoted_order_id).\
    values('item__category__name', 'item__category', 'item__category__unit',
        'item__category__unit__unit').\
    order_by('item__category').distinct()
    quoted_item_obj = QuotedItem.objects.filter(quoted_order=quoted_order_id).\
    values('item__name',\
    'item__category', 'qty', 'price_per_unit').order_by('item__category')
    cost = QuotedItem.objects.filter(quoted_order=quoted_order_id).\
    values('price', 'item__category', 'item__name').order_by('item__category')
    quoted_order_sessionid = QuotedOrderofSession.objects.filter\
    (quoted_order_id=quoted_order_id).values('quoted_order_session')[0]
    bill_values = []
    for category in quoted_item:
        flag1 = 1
        list = []
        list.append(category['item__category__name'])
        item_names = []
        for item in quoted_item_obj:
            if category['item__category'] == item['item__category']:
                if flag1 == 1:
                    item_names.append(':')
                    item_names.append(item['item__name'])
                    flag1 = 0
                else:
                    item_names.append(',')
                    item_names.append(item['item__name'])
        flag1 = 1
        item_qty = []
        for qty in quoted_item_obj:
            if category['item__category'] == qty['item__category']:
                if flag1 == 1:
                    item_qty.append(qty['qty'])
                    flag1 = 0
                else:
                    item_qty.append(',')
                    item_qty.append(qty['qty'])
        if category['item__category__unit']:
            item_qty.append(category['item__category__unit__unit'])
        else:
            item_qty.append('no_unit')
        flag1 = 1
        price_unit = []
        for price_per in quoted_item_obj:
            if category['item__category'] == price_per['item__category']:
                if flag1 == 1:
                    price_unit.append(price_per['price_per_unit'])
                    flag1 = 0
                else:
                    price_unit.append(',')
                    price_unit.append(price_per['price_per_unit'])
        total = 0
        for itemcost in cost:
            if category['item__category'] == itemcost['item__category']:
                total = total + itemcost['price']
        list.append(item_names)
        list.append(item_qty)
        list.append(price_unit)
        list.append(total)
        bill_values.append(list)
    taxes_applied = QuotedTaxesApplied.objects.\
    filter(quoted_order=quoted_order).values('surcharge', 'tax', 'surcharge_name',
        'surcharge_value')
    taxes_applied_obj = QuotedTaxesApplied.objects.\
    filter(quoted_order=quoted_order).aggregate(Count('id'))
    bill = QuotedBill.objects.values('total_cost', 'grand_total',\
        'delivery_charges', 'totalplusdelivery').get(quoted_order=quoted_order_id)
    total_cost = bill['total_cost']
    grand_total = bill['grand_total']
    delivery_charges = bill['delivery_charges']
    totalplusdelivery = bill['totalplusdelivery']
    quoted_order_obj = QuotedOrder.objects.values('buyer','buyer__first_name',\
        'buyer__last_name','reference','delivery_address','organisation',\
        'date_time','total_discount','buyer__customer__title',\
        'reference_date').get(id = quoted_order_id)
    total_discount = quoted_order_obj['total_discount']
    taxes_applied_obj = QuotedTaxesApplied.objects.\
    filter(quoted_order=quoted_order).aggregate(Count('id'))
    try:
        suspense_order = QuotedSuspenseOrder.objects.\
        values('distance_estimated').get(quoted_order=quoted_order_id)
        if suspense_order['distance_estimated'] == 0:
            if total_discount == 0:
                tax_count = taxes_applied_obj['id__count'] + 2
            else:
                tax_count = taxes_applied_obj['id__count'] + 3
        else:
            if total_discount == 0:
                tax_count = taxes_applied_obj['id__count'] + 4
            else:
                tax_count = taxes_applied_obj['id__count'] + 5
    except:
        if total_discount == 0:
            tax_count = taxes_applied_obj['id__count'] + 2
        else:
            tax_count = taxes_applied_obj['id__count'] + 3
    if taxes_applied_obj['id__count'] == 0:
        tax_count = tax_count + 1
    buyer = quoted_order_obj['buyer']
    address = Customer.objects.values('address__street_address',\
    'address__district', 'address__pin', 'address__province').get(user=buyer)
    organisation_id = quoted_order_obj['organisation']
    date = quoted_order_obj['date_time']
    customer_obj = Customer.objects.values('company').get(user=buyer)
    admin_organisations = AdminOrganisations.objects.values('pan_no',\
        'stc_no', 'gst_in').get(id = organisation_id)
    header = HeaderFooter.objects.values('header').get(is_active=True)
    footer = HeaderFooter.objects.values('footer').get(is_active=True)
    permanent_note = NoteLine.objects.values('note').filter(is_permanent=True)
    quoted_note = QuotedOrderNote.objects.values('note').\
    filter(quoted_order=quoted_order_id)
    account_holder = _ACCOUNT_HOLDER
    name_of_bank = _NAME_OF_BANK
    branch = _BRANCH
    online_account = _ONLINE_ACCOUNT
    ifsc_code = _IFSC_CODE
    ref_letter = _YOUR_LETTER_No
    total_in_words = num2eng(grand_total)
    return render(request, 'bills/quote_bill.html', {
        'admin_org': admin_organisations,\
        'ref':quoted_order_obj, 'date':date,\
        'quoted_order':quoted_order, 'address':address,\
        'total_cost': total_cost, 'grand_cost':grand_total,\
        'taxes_applied': taxes_applied,\
        'buyer':quoted_order_obj, 'buyer_name':customer_obj,\
        'site': quoted_order_obj, 'delivery_charges':delivery_charges,\
        'total_discount':total_discount, 'tax_count':tax_count,\
        'bill_values':bill_values, 'total_in_words':total_in_words,\
        'quoted_order_id':quoted_order_sessionid['quoted_order_session'],\
        'header':header,'footer':footer, 'permanent_note':permanent_note,\
        'quoted_note':quoted_note, 'account_holder':account_holder,\
        'name_of_bank':name_of_bank, 'branch':branch,\
        'online_account':online_account, 'ifsc_code':ifsc_code,\
        'totalplusdelivery':totalplusdelivery, 'ref_letter':ref_letter})
