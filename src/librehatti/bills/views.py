from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect

from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import Category
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import ModeOfPayment
from librehatti.catalog.models import Product
from librehatti.catalog.models import HeaderFooter
from librehatti.catalog.models import Surcharge
from librehatti.catalog.models import SpecialCategories
from librehatti.catalog.request_change import request_notify

from librehatti.bills.models import QuotedTaxesApplied
from librehatti.bills.models import QuotedOrder
from librehatti.bills.models import QuotedBill
from librehatti.bills.models import QuotedItem
from librehatti.bills.models import QuotedOrderofSession
from librehatti.bills.models import QuotedOrderNote
from librehatti.bills.models import NoteLine
from librehatti.bills.forms import SelectNoteForm
from librehatti.bills.forms import ItemSelectForm

from librehatti.suspense.models import QuotedSuspenseOrder

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

import useraccounts

from django.db.models import Sum
from django.db.models import Max

import simplejson

from django.urls import reverse

from librehatti.voucher.models import FinancialSession


@login_required
def quoted_bill_cal(request):
    """
    This view calculate taxes on quoted order, bill data
    and save those values in database.
    argument: Http request
    returns: Redirects to select option page after calculatations. 
    """
    old_post = request.session.get('old_post')
    quoted_order_id = request.session.get('quoted_order_id')
    generate_tax = 1
    first_item = QuotedItem.objects.values('item__category__id').\
    filter(quoted_order=quoted_order_id)[0]
    category_check = SpecialCategories.objects.filter(category=
        first_item['item__category__id'])
    if category_check:
        specialcategories = SpecialCategories.objects.values('tax').\
        filter(category=first_item['item__category__id'])[0]
        if specialcategories['tax'] == False:
            generate_tax = 0
    quoted_order = QuotedOrder.objects.get(id=quoted_order_id)
    quoted_order_obj = QuotedOrder.objects.values('total_discount').\
    get(id=quoted_order_id)
    quoted_item = QuotedItem.objects.\
    filter(quoted_order=quoted_order_id).aggregate(Sum('price'))
    total = quoted_item['price__sum']
    price_total = total - quoted_order_obj['total_discount']
    totalplusdelivery = price_total
    surcharge = Surcharge.objects.values('id', 'value', 'taxes_included', 'tax_name')
    delivery_rate = Surcharge.objects.values('value').\
    filter(tax_name='Transportation')
    distance = QuotedSuspenseOrder.objects.\
    filter(quoted_order=quoted_order_id).aggregate(Sum('distance_estimated'))
    if distance['distance_estimated__sum']:
        delivery_charges = int(distance['distance_estimated__sum'])*\
            delivery_rate[0]['value']
        totalplusdelivery = totalplusdelivery + delivery_charges

    else:
        delivery_charges = 0

    for value in surcharge:
        surcharge_id = value['id']
        surcharge_val = value['value']
        surcharge_tax = value['taxes_included']
        if surcharge_tax == 1 and generate_tax == 1:
            taxes = round((totalplusdelivery * surcharge_val)/100)
            surcharge_obj = Surcharge.objects.get(id=surcharge_id)
            taxes_applied = QuotedTaxesApplied(quoted_order=quoted_order,
            surcharge=surcharge_obj, tax=taxes, surcharge_name = value['tax_name'],
                surcharge_value = value['value'])
            taxes_applied.save()
    taxes_applied_temp = QuotedTaxesApplied.objects.\
    filter(quoted_order=quoted_order_id)
    if taxes_applied_temp:
        taxes_applied_obj = QuotedTaxesApplied.objects.\
        filter(quoted_order=quoted_order_id).aggregate(Sum('tax'))
        tax_total = taxes_applied_obj['tax__sum']
    else:
        tax_total = 0
    grand_total = price_total + tax_total + delivery_charges
    amount_received = grand_total
    bill = QuotedBill(quoted_order=quoted_order, total_cost=price_total,
    total_tax=tax_total, grand_total=grand_total,
    delivery_charges=delivery_charges, amount_received=amount_received,
    totalplusdelivery=totalplusdelivery)
    bill.save()
    request.session['old_post'] = old_post
    request.session['quoted_order_id'] = quoted_order_id
    return HttpResponseRedirect(reverse("bills:select_note"))


@login_required
def quoted_order_added_success(request):
    """
    View to hadle success of addition of quoted order.
    argument: Http request
    returns: Render success page after adding quoted order.
    """
    quoted_order_id = request.session.get('quoted_order_id')
    details = QuotedOrder.objects.values('buyer__first_name',\
        'buyer__last_name', 'buyer__customer__address__street_address',\
        'buyer__customer__title', 'buyer__customer__address__district').\
    filter(id=quoted_order_id)[0]
    return render(request, 'bills/quoted_success.html', {'details':details,
        'quoted_order_id':quoted_order_id})


@login_required
def select_note(request):
    """
    View to handle selection of extra notes while adding quoted order.
    argument: Http Request.
    returns: Render form for selection of note form.
    """
    quoted_order_id = request.session.get('quoted_order_id')
    form = SelectNoteForm(initial={'quoted_order':quoted_order_id})
    request_status = request_notify()
    return render(request, 'bills/select_note.html', \
        {'form':form, 'request':request_status})


@login_required
def select_note_save(request):
    """
    View to hanle saving of selected note in quoted order.
    argument: Http Request
    returns: Redirects to success page after selection of note line.
    """
    if request.method == 'POST':
        form = SelectNoteForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            quoted_order = formdata['quoted_order']
            quoted_order_id = QuotedOrder.objects.get(id=quoted_order)
            note_list = []
            for note in formdata['note_line']:
                note_list.append(note)
            for value in note_list:
                obj = QuotedOrderNote(quoted_order=quoted_order_id, note=value)
                obj.save()

            return HttpResponseRedirect(\
                reverse("bills:quoted_order_added_success"))
        else:
            return HttpResponseRedirect(\
                reverse("bills:quoted_order_added_success"))
    else:
        error_type = "404 Forbidden"
        error = "Please again place the order"
        temp = {'type': error_type, 'message':error}
        return render(request, 'error_page.html', temp)


@login_required
def new_note_line(request):
    """
    It hanles addition of new condition line.
    argument: Http Request
    """
    note_line = request.GET['note_line']
    obj = NoteLine(note=note_line)
    obj.save()
    return HttpResponse('')


@login_required
def delete_note(request):
    """
    It handles deletion of condition line.
    argument: Http Request.
    """
    delete_note = request.GET['delete_note']
    delete_note_id = delete_note.split(',')
    for id in delete_note_id:
        NoteLine.objects.filter(id=id).delete()
    return HttpResponse('')


@login_required
def quoted_order_of_session(request):
    """
    It handles financial sessions for quoted order.
    argument: Http Request
    returns: Redirects to function for adding quoted add distance.
    """
    old_post = request.session.get('old_post')
    quoted_order_id = request.session.get('quoted_order_id')
    quoted_order = QuotedOrder.objects.get(id=quoted_order_id)
    quoted_order_obj = QuotedOrder.objects.values('id', 'date_time').\
    get(id=quoted_order_id)
    quoted_order_date = quoted_order_obj['date_time']
    financialsession = FinancialSession.objects.\
    values('id', 'session_start_date', 'session_end_date')
    for value in financialsession:
        start_date = value['session_start_date']
        end_date = value['session_end_date']
        if start_date <= quoted_order_date <= end_date:
            session_id = value['id']
    session = FinancialSession.objects.get(id=session_id)
    max_id = QuotedOrderofSession.objects.all().aggregate(Max('id'))
    if max_id['id__max'] == None:
        obj = QuotedOrderofSession(quoted_order=quoted_order,\
            session=session, quoted_order_session=1)
        obj.save()
    else:
        quoted_order_of_session = QuotedOrderofSession.objects.\
        values('quoted_order_session', 'session').get(id=max_id['id__max'])
        if quoted_order_of_session['session'] == session_id:
            obj = QuotedOrderofSession(quoted_order=quoted_order,\
            session=session, quoted_order_session=\
            quoted_order_of_session['quoted_order_session']+1)
            obj.save()
        else:
            obj = QuotedOrderofSession(quoted_order=quoted_order,\
            session=session, quoted_order_session=1)
            obj.save()
    request.session['old_post'] = old_post
    request.session['quoted_order_id'] = quoted_order_id
    return HttpResponseRedirect(\
        reverse("suspense:quoted_add_distance"))
