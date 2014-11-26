from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import Category
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import ModeOfPayment
from librehatti.catalog.models import Product
from librehatti.catalog.models import HeaderFooter
from librehatti.catalog.models import Surcharge
from librehatti.bills.models import QuotedTaxesApplied
from librehatti.bills.models import QuotedOrder
from librehatti.bills.models import QuotedBill
from librehatti.bills.models import QuotedItem
from librehatti.bills.models import QuotedOrderNote
from librehatti.bills.models import NoteLine
from librehatti.suspense.models import QuotedSuspenseOrder
from django.contrib.auth.models import User
import useraccounts
from django.db.models import Sum
from librehatti.bills.forms import SelectNoteForm
from django.db.models import Max
import simplejson
from django.contrib.auth.decorators import login_required
from librehatti.bills.forms import ItemSelectForm
from django.core.urlresolvers import reverse
from librehatti.catalog.request_change import request_notify

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
    return HttpResponseRedirect(reverse("librehatti.bills.views.select_note"))


@login_required
def quoted_order_added_success(request):
    quoted_order_id = request.session.get('quoted_order_id')
    details = QuotedOrder.objects.values('buyer__first_name','buyer__last_name'
        ,'buyer__customer__address__street_address','buyer__customer__title',
        'buyer__customer__address__city','mode_of_payment__method',
        'cheque_dd_number','cheque_dd_date').filter(id=quoted_order_id)[0]
    return render(request,'bills/quoted_success.html',{'details': details,
        'quoted_order_id':quoted_order_id})


@login_required
def select_note(request):
    quoted_order_id = request.session.get('quoted_order_id')
    form = SelectNoteForm(initial={'quoted_order':quoted_order_id})
    request_status = request_notify()
    return render(request, 'bills/select_note.html', \
        {'form':form,'request':request_status})


@login_required
def select_note_save(request):
    if request.method == 'POST':
        form = SelectNoteForm(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            quoted_order = formdata['quoted_order']
            quoted_order_id = QuotedOrder.objects.get(id=quoted_order)
            note_list=[]
            for note in formdata['note_line']:
                note_list.append(note)
            for value in note_list:
                obj=QuotedOrderNote(quoted_order=quoted_order_id,note=value)
                obj.save()

            return HttpResponseRedirect(\
                reverse("librehatti.bills.views.quoted_order_added_success"))
        else:
            return HttpResponseRedirect(\
                reverse("librehatti.bills.views.quoted_order_added_success"))
    else:
        error_type = "404 Forbidden"
        error = "Please again place the order"
        temp = {'type': error_type, 'message':error}
        return render(request, 'error_page.html', temp)


@login_required
def new_note_line(request):
    note_line = request.GET['note_line']
    obj = NoteLine(note=note_line)
    obj.save()
    return HttpResponse('')

@login_required
def delete_note(request):
    delete_note = request.GET['delete_note']
    delete_note_id = delete_note.split(',')
    for id in delete_note_id:
        NoteLine.objects.filter(id=id).delete()
    return HttpResponse('')
