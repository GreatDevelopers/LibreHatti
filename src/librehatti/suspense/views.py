from django.shortcuts import render

from django.db.models import Sum, Max

from .models import SuspenseClearance
from .models import TaDa, TaDa_Tax_Detail

from django.http import  HttpResponseRedirect, HttpResponse

from django.urls import reverse

from librehatti.catalog.models import Product
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import Surcharge
from librehatti.catalog.models import HeaderFooter
from librehatti.catalog.models import SpecialCategories
from librehatti.catalog.request_change import request_notify

from librehatti.suspense.models import SuspenseClearance
from librehatti.suspense.models import SuspenseOrder
from librehatti.suspense.models import Transport
from librehatti.suspense.models import QuotedSuspenseOrder
from librehatti.suspense.models import Vehicle
from librehatti.suspense.models import Staff, CarTaxiAdvance
from librehatti.suspense.models import TransportBillOfSession
from librehatti.suspense.models import SuspenseClearedRegister
from librehatti.suspense.forms import Clearance_form
from librehatti.suspense.forms import SuspenseForm
from librehatti.suspense.forms import QuotedSuspenseForm
from librehatti.suspense.forms import TaDaForm
from librehatti.suspense.forms import TaDaSearch
from librehatti.suspense.forms import SessionSelectForm
from librehatti.suspense.forms import TransportForm1
from librehatti.suspense.forms import CarTaxiAdvance_form

from librehatti.prints.helper import num2eng

from librehatti.bills.models import QuotedOrder
from librehatti.bills.models import QuotedItem

from librehatti.voucher.models import VoucherId, Distribution
from librehatti.voucher.models import FinancialSession, CalculateDistribution
from librehatti.voucher.models import VoucherTotal

from librehatti.reports.forms import DateRangeSelectionForm

from django.contrib.auth.decorators import login_required

import simplejson
import json
from datetime import date, datetime

from django.template.loader import get_template
from django.template import Context

@login_required
def add_distance(request):
    """
    Handles add suspense order. It also decide whether order suspense or not.
    argument: Http Request
    return: Check for type of order and redirects accordingly.
        Types of Order:
            1.Main
            2.Suspense
    """
    old_post = request.session.get('old_post')
    purchase_order_id = request.session.get('purchase_order_id')
    items = []
    parents = []
    field_work = []
    suspense = 0
    generate_voucher = 1
    first_item = PurchasedItem.objects.values('item__category__id').\
    filter(purchase_order=purchase_order_id)[0]
    category_check = SpecialCategories.objects.filter(category=
        first_item['item__category__id'])
    if category_check:
        specialcategories = SpecialCategories.objects.values('voucher').\
        filter(category=first_item['item__category__id'])[0]
        if specialcategories['voucher'] == False:
            generate_voucher = 0
    for id in range(0,10):
        try:
            items.append(old_post['purchaseditem_set-' + str(id) + '-item'])
        except:
            pass
    for item in items:
        if item:
            parents.append(PurchasedItem.objects.values(
              'item__category__parent__name','id').filter(item=item).\
              filter(purchase_order=purchase_order_id))
    for parent in parents:
        if generate_voucher == 0:
            break
        for category in parent:
            value = category['item__category__parent__name']
            key = category['id']
            temp_val = value.split(':')
            try:
                if temp_val[1].upper() == 'FIELD WORK' or \
                    temp_val[1].upper() == ' FIELD WORK':
                    field_work.append(key)
            except:
                pass
    if field_work and generate_voucher == 1:
        if request.method == 'POST':
            request.session['old_post'] = old_post
            request.session['purchase_order_id'] = purchase_order_id
            return HttpResponseRedirect(\
                reverse("catalog:bill_cal"))
        else:
            purchase_order = PurchaseOrder.objects.values('date_time').\
                get(id=purchase_order_id)
            purchase_order_obj = PurchaseOrder.objects.get(id=purchase_order_id)
            purchase_order_date = purchase_order['date_time']
            financialsession = FinancialSession.objects.\
                values('id', 'session_start_date', 'session_end_date')
            for value in financialsession:
                start_date = value['session_start_date']
                end_date = value['session_end_date']
                if start_date <= purchase_order_date <= end_date:
                    session_id = value['id']
            financial_obj = FinancialSession.objects.get(id=session_id)
            voucher = VoucherId.objects.values('voucher_no',
                'purchased_item__item__category__name').\
                filter(purchase_order=purchase_order_id).\
                filter(session=session_id).distinct()
            for voucher_val in voucher:
                suspense_check = SuspenseOrder.objects.filter(
                voucher=voucher_val['voucher_no'],session_id = financial_obj)
                if not suspense_check:
                    suspense_obj = SuspenseOrder(voucher=voucher_val['voucher_no'],\
                        purchase_order=purchase_order_obj, session_id=financial_obj)
                    suspense_obj.save()
            return render(request,'suspense/add_distance.html',{
                'voucher':voucher, 'purchase_order_id': purchase_order_id})
    elif old_post['mode_of_payment'] != '1' and generate_voucher == 1:
        purchase_order = PurchaseOrder.objects.values('date_time').\
            get(id=purchase_order_id)
        purchase_order_date = purchase_order['date_time']
        financialsession = FinancialSession.objects.\
            values('id', 'session_start_date', 'session_end_date')
        for value in financialsession:
            start_date = value['session_start_date']
            end_date = value['session_end_date']
            if start_date <= purchase_order_date <= end_date:
                session_id = value['id']
        session = FinancialSession.objects.get(pk=session_id)
        voucher = VoucherId.objects.values('voucher_no').\
            filter(purchase_order=purchase_order_id).distinct()
        order = PurchaseOrder.objects.get(pk=purchase_order_id)
        for voucher_no in voucher:
            suspense = SuspenseOrder(voucher=voucher_no['voucher_no'],
            purchase_order=order, session_id=session, distance_estimated = 0)
            suspense.save()
        request.session['old_post'] = old_post
        request.session['purchase_order_id'] = purchase_order_id
        return HttpResponseRedirect(\
            reverse("catalog:bill_cal"))
    else:
        request.session['old_post'] = old_post
        request.session['purchase_order_id'] = purchase_order_id
        return HttpResponseRedirect(\
            reverse("catalog:bill_cal"))


@login_required
def clearance_search(request):
    """
    Handles clrearance search.
    argument: Http Request
    returns: Objects for entered session and order.
    It also render form for Clearance.
    """
    if request.method == 'POST':
        sessiondata = SessionSelectForm(request.POST)
        if sessiondata.is_valid():
            voucher = sessiondata.data['voucher']
            session = sessiondata.data['session']
            object = SuspenseOrder.objects.filter(session_id=session).\
            filter(voucher=voucher).values()
            if object:
                form = Clearance_form(initial={'voucher_no':voucher,\
                'session':session, 'labour_charge':0, 'car_taxi_charge':0,\
                'boring_charge_external':0, 'boring_charge_internal':0})
                clearance = 'enable'
                session_data = FinancialSession.objects.values(\
                    'session_start_date','session_end_date').get(id=session)
                messages = " Voucher" + " : " + voucher + " and Session" + " : " +\
                    str(session_data['session_start_date']) + ":" +\
                    str(session_data['session_end_date'])
                request_status = request_notify()
                return render(request, 'suspense/suspense_first.html', \
                    {'form':form, 'clearance':clearance,\
                    'messages':messages, 'request':request_status})
            else:
                form = SessionSelectForm()
                errors = "No such voucher number in selected session"
                request_status = request_notify()
                temp = {"form":form , "message":errors,\
                'request':request_status}
                return render(request, 'suspense/suspense_first.html', temp)
        else:
            form = SessionSelectForm(request.POST)
            request_status = request_notify()
            return render(request, 'suspense/suspense_first.html',\
                {'form':form, 'request':request_status})
    else:
        form = SessionSelectForm()
        request_status = request_notify()
        return render(request, 'suspense/suspense_first.html',\
            {'form':form, 'request':request_status})


@login_required
def clearance_result(request):
    """
    Handles result of clearance search.
    argument: Http Request
    returns: Success page with required values.
    """
    if request.method == 'POST':
        form = Clearance_form(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            voucher_no = formdata['voucher_no']
            session = formdata['session']
            labour_charge = formdata['labour_charge']
            car_taxi_charge = formdata['car_taxi_charge']
            boring_charge_external = formdata['boring_charge_external']
            boring_charge_internal = formdata['boring_charge_internal']
            lab_testing_staff = formdata['lab_testing_staff']
            field_testing_staff = formdata['field_testing_staff']
            test_date = formdata['test_date']
            clear_date = formdata['clear_date']
            session_id = str(session)
            split = session_id.split(' : ')
            start_date = datetime.strptime(split[0], '%Y-%m-%d').date()
            end_date = datetime.strptime(split[1], '%Y-%m-%d').date()
            financialsession = FinancialSession.objects.values('id').\
            get(session_start_date=start_date, session_end_date=end_date)
            suspense_object = SuspenseOrder.objects.filter(voucher=voucher_no,\
                session_id=session).update(is_cleared=0)
            try:
                SuspenseClearance.objects.get(voucher_no=voucher_no,\
                    session=financialsession['id'])
                SuspenseClearance.objects.\
                filter(voucher_no=voucher_no, session=financialsession['id']).\
                update(session=session, voucher_no=voucher_no,\
                    work_charge=0, labour_charge=labour_charge,\
                    car_taxi_charge=car_taxi_charge,\
                    boring_charge_external=boring_charge_external,\
                    boring_charge_internal=boring_charge_internal,\
                    lab_testing_staff=lab_testing_staff,\
                    field_testing_staff=field_testing_staff,\
                    test_date=test_date, clear_date=clear_date)
            except:
                obj= SuspenseClearance(session=session, voucher_no=voucher_no,
                     work_charge=0, labour_charge=labour_charge,
                     car_taxi_charge=car_taxi_charge,
                     boring_charge_external=boring_charge_external,
                     boring_charge_internal=boring_charge_internal,
                     lab_testing_staff=lab_testing_staff,
                     field_testing_staff=field_testing_staff,
                     test_date=test_date, clear_date=clear_date)
                obj.save()
            request_status = request_notify()
            temp = {'session':session,'voucher_no': voucher_no,\
                    'labour_charge':labour_charge,\
                    'car_taxi_charge':car_taxi_charge,
                    'boring_charge_external':boring_charge_external,
                    'boring_charge_internal':boring_charge_internal,
                    'lab_testing_staff':lab_testing_staff,
                    'field_testing_staff':field_testing_staff,\
                    'test_date':test_date, 'clear_date':clear_date,\
                    'request':request_status}
            return render(request, 'suspense/clearance_result.html', temp)
        else:
            voucher = request.POST['voucher_no']
            session = request.POST['session']
            transport = Transport.objects.values('total').\
            get(voucher_no=voucher, session=session)
            form = Clearance_form(request.POST,initial={'voucher_no': voucher,\
            'session': session, 'car_taxi_charge':transport['total']})
            clearance = 'enable'
            message = "Fields are mandatory"
            request_status = request_notify()
            return render(request, 'suspense/suspense_first.html', \
                {'form':form, 'clearance':clearance, 'message':message,
                'request':request_status})
    else:
        return HttpResponseRedirect(\
            reverse('suspense:clearance_search'))


@login_required
def with_transport(request):
    """
    Handles bills with transport.
    argument: Http Request
    returns: Render bill without transport.
    """
    number = request.GET['voucher_no']
    session = request.GET['session']
    financialsession = FinancialSession.objects.values('id').\
    get(id=session)
    try:
        transport = Transport.objects.values('total').get(voucher_no=number,\
            session=financialsession['id'])
        transport_total = transport['total']
    except:
        transport_total = 0

    tada = TaDa.objects.values_list('tada_amount',flat=True).filter(voucher_no=number,\
        session=financialsession['id'])
    tada_amount = 0
    for value in tada:
        tada_amount = tada_amount + value

    suspenseclearance = SuspenseClearance.objects.values('work_charge',\
    'labour_charge', 'car_taxi_charge', 'boring_charge_internal',\
    'boring_charge_external', 'lab_testing_staff', 'field_testing_staff',\
    'test_date', 'clear_date').\
    get(voucher_no=number, session=financialsession['id'])
    othercharge = transport_total + suspenseclearance['labour_charge'] +\
    suspenseclearance['car_taxi_charge'] +\
    suspenseclearance['boring_charge_external']
    boring_charge_internal = suspenseclearance['boring_charge_internal']
    lab_staff_list = suspenseclearance['lab_testing_staff'].split(',')
    lab_staff_name_list = []
    if lab_staff_list[0]:
        for lab_staff_value in lab_staff_list:
            lab_temp = []
            lab_staff_obj = Staff.objects.values('name', 'position__position').\
            filter(code=lab_staff_value)[0]
            lab_temp.append(lab_staff_obj['name'])
            lab_temp.append(lab_staff_obj['position__position'])
            lab_staff_name_list.append(lab_temp)
    field_staff_list = suspenseclearance['field_testing_staff'].split(',')
    field_staff_name_list = []
    if field_staff_list[0]:
        for field_staff_value in field_staff_list:
            field_temp = []
            field_staff_obj = Staff.objects.values('name','position__position').\
            filter(code=field_staff_value)[0]
            field_temp.append(field_staff_obj['name'])
            field_temp.append(field_staff_obj['position__position'])
            field_staff_name_list.append(field_temp)
    ta_da_total = tada_amount
    voucherid = VoucherId.objects.values('ratio', 'purchase_order_of_session',\
    'purchase_order__date_time', 'purchase_order__buyer__first_name',\
    'purchase_order__buyer__last_name', 'purchase_order__mode_of_payment',\
    'purchase_order__buyer__customer__address__street_address',\
    'purchase_order__buyer__customer__address__district',\
    'purchase_order__buyer__customer__address__pin',\
    'purchase_order__buyer__customer__address__province','college_income',\
    'admin_charges', 'purchase_order__cheque_dd_number',\
    'purchase_order__cheque_dd_date','purchase_order__mode_of_payment__method',\
    'purchase_order__buyer__customer__title',
    'purchased_item__item__category__name').filter(voucher_no=number,\
    session=financialsession['id'])[0]
    distribution = Distribution.objects.values('name').\
    get(ratio=voucherid['ratio'])
    calculate_distribution = CalculateDistribution.objects.\
    values('college_income_calculated', 'admin_charges_calculated',\
    'consultancy_asset', 'development_fund', 'total').\
    get(voucher_no=number, session=financialsession['id'])
    total = calculate_distribution['total'] + othercharge + ta_da_total +\
    suspenseclearance['work_charge'] + boring_charge_internal
    total_in_words = num2eng(total)
    rowspan = 6
    if suspenseclearance['work_charge'] == 0:
        rowspan = rowspan - 1
    if ta_da_total != 0:
        rowspan = rowspan + 1
    if othercharge != 0:
        rowspan = rowspan + 1
    if suspenseclearance['boring_charge_internal'] != 0:
        rowspan = rowspan + 1
    sus_cleared_reg = SuspenseClearedRegister.objects.filter(voucher_no=number, session_id=session)[0]
    header = HeaderFooter.objects.values('header').get(is_active=True)
    return render(request,'suspense/with_transport.html', {'header':header,\
                'voucher_no':number, 'date':suspenseclearance['clear_date'],\
                'calculate_distribution':calculate_distribution,\
                'suspense_clearance':suspenseclearance,\
                'field_staff':field_staff_name_list,\
                'lab_staff':lab_staff_name_list, 'ratio':voucherid['ratio'],\
                'distribution':distribution['name'],\
                'purchase_order':voucherid['purchase_order_of_session'],\
                'order_date':voucherid['purchase_order__date_time'],\
                'address':voucherid, 'ta_da':ta_da_total,\
                'othercharge':othercharge, 'total':total,\
                'total_in_words':total_in_words,\
                'test_date':suspenseclearance['test_date'],\
                'charges':voucherid, 'rowspan':rowspan, 'payment':voucherid,
                'sus_cleared_reg':sus_cleared_reg})


@login_required
def other_charges(request):
    """
    Handles other charges of bills.
    argument: Http Request
    returns: render detail page of other charges.
    """
    number = request.GET['voucher_no']
    session = request.GET['session']
    financialsession = FinancialSession.objects.values('id').\
    get(id=session)
    try:
        transport = Transport.objects.values('id','date_of_generation','total').\
        get(voucher_no=number, session=financialsession['id'])
        transport_total = transport['total']
        transportbillno = TransportBillOfSession.objects.values(
            'transportbillofsession').get(transport__voucher_no=number,
            transport__session=session)
    except:
        transport_total = 0
        transport = 0
        transportbillno = 0
    suspenseclearance = SuspenseClearance.objects.values('work_charge',\
    'boring_charge_internal', 'boring_charge_external', 'labour_charge',\
    'car_taxi_charge', 'field_testing_staff', 'lab_testing_staff',\
    'clear_date', 'test_date').get(voucher_no=number, session=financialsession['id'])

    tada = TaDa.objects.values_list('tada_amount',flat=True).filter(voucher_no=number,\
        session=financialsession['id'])
    ta_da_total = 0
    for value in tada:
        ta_da_total = ta_da_total + value
    voucherid = VoucherId.objects.values('ratio','purchase_order_of_session',\
    'purchase_order__date_time', 'purchase_order__buyer__first_name',\
    'purchase_order__buyer__last_name',\
    'purchase_order__buyer__customer__address__street_address',\
    'purchase_order__buyer__customer__address__district',\
    'purchase_order__buyer__customer__address__pin',\
    'purchase_order__buyer__customer__address__province',\
    'purchase_order__buyer__customer__title').filter(voucher_no=number,\
    session=financialsession['id'])[0]
    other_charges = suspenseclearance['boring_charge_external'] +\
    suspenseclearance['car_taxi_charge'] +\
    suspenseclearance['labour_charge']
    total = other_charges + ta_da_total
    complete_total = total + transport_total
    transplusother = other_charges + transport_total
    header = HeaderFooter.objects.values('header').get(is_active=True)
    car_taxi_advance_obj = CarTaxiAdvance.objects.filter(voucher_no=number,
        session=session)
    if car_taxi_advance_obj:
        car_taxi_advance = CarTaxiAdvance.objects.values('spent', 'advance',
            'balance', 'receipt_no', 'receipt_session').get(voucher_no=number,
            session=session)
        receipt_dated = VoucherId.objects.values('purchase_order__date_time').filter(
            receipt_no_of_session=car_taxi_advance['receipt_no'],
            session_id=car_taxi_advance['receipt_session'])[0]
        return render(request,'suspense/othercharge.html', {'header':header,\
                    'voucher_no':number, 'date':suspenseclearance['clear_date'],\
                    'suspense_clearance':suspenseclearance,\
                    'purchase_order':voucherid['purchase_order_of_session'],\
                    'order_date':voucherid['purchase_order__date_time'],\
                    'address':voucherid, 'ta_da':ta_da_total,\
                    'boring_charges':suspenseclearance['boring_charge_external'],\
                    'total':total, 'other_charges':other_charges,\
                    'transport':transport, 'complete_total':complete_total,\
                    'transplusother':transplusother,
                    'transportbillno':transportbillno,
                    'test_date':suspenseclearance['test_date'],
                    'receipt_dated':receipt_dated,
                    'car_taxi_advance':car_taxi_advance})
    else:
        return render(request,'suspense/othercharge.html', {'header':header,\
                    'voucher_no':number, 'date':suspenseclearance['clear_date'],\
                    'suspense_clearance':suspenseclearance,\
                    'purchase_order':voucherid['purchase_order_of_session'],\
                    'order_date':voucherid['purchase_order__date_time'],\
                    'address':voucherid, 'ta_da':ta_da_total,\
                    'boring_charges':suspenseclearance['boring_charge_external'],\
                    'total':total, 'other_charges':other_charges,\
                    'transport':transport, 'complete_total':complete_total,\
                    'transplusother':transplusother,
                    'transportbillno':transportbillno,
                    'test_date':suspenseclearance['test_date']})


@login_required
def suspense(request):
    """
    argument: Http Request
    returns: render SuspenseForm.
    """
    form = SuspenseForm()
    return render(request,'suspense/form.html',{'form':form})


@login_required
def save_charges(request):
    """
    Saves estimated charges for suspense order.
    argument: Http Request
    """
    if request.method=='GET':
        option=request.GET['Purchase_order']
        charges=request.GET['distance']
        obj = SuspenseOrder(purchase_order_id=option,transportation=charges)
        obj.save()
        return HttpResponse('Thanks!')


@login_required
def quoted_add_distance(request):
    """
    Handles estimated distance for quoted order.
    argument: Http Request
    returns: check type of quoted order and redirects accordingly.
    """
    old_post = request.session.get('old_post')
    quoted_order_id = request.session.get('quoted_order_id')
    items = []
    parents = []
    field_work = []
    suspense = 0
    generate_voucher = 1
    first_item = QuotedItem.objects.values('item__category__id').\
    filter(quoted_order=quoted_order_id)[0]
    category_check = SpecialCategories.objects.filter(category=
        first_item['item__category__id'])
    if category_check:
        specialcategories = SpecialCategories.objects.values('voucher').\
        filter(category=first_item['item__category__id'])[0]
        if specialcategories['voucher'] == False:
            generate_voucher = 0
    for id in range(0,10):
        try:
            items.append(old_post['quoteditem_set-' + str(id) + '-item'])
        except:
            pass
    for item in items:
        if item:
            parents.append(QuotedItem.objects.values(
              'item__category__parent__name','id').filter(item=item).\
              filter(quoted_order=quoted_order_id))
    for parent in parents:
        if generate_voucher == 0:
            break
        for category in parent:
            value = category['item__category__parent__name']
            key = category['id']
            if value.split(':')[1].upper() == 'FIELD WORK' or \
                value.split(':')[1].upper() == ' FIELD WORK':
                field_work.append(key)
    if field_work and generate_voucher == 1:
        if request.method == 'POST':
            request.session['old_post'] = old_post
            request.session['quoted_order_id'] = quoted_order_id
            return HttpResponseRedirect(\
                reverse("bills:quoted_bill_cal"))
        else:
            return render(request,'suspense/quoted_add_distance.html',{\
                'quoted_order_id':quoted_order_id,})
    else:
        request.session['old_post'] = old_post
        request.session['quoted_order_id'] = quoted_order_id
        return HttpResponseRedirect(\
            reverse("bills:quoted_bill_cal"))


@login_required
def quoted_save_distance(request):
    """
    Saves estimated distance for quoted order.
    argument: Http Request
    returns:None
    """
    quoted_order_id = request.GET['quoted_order_id']
    distance = request.GET['distance']
    quoted_order = QuotedOrder.objects.get(pk=quoted_order_id)
    try:
        suspense = QuotedSuspenseOrder.objects.get(quoted_order=quoted_order_id)
        suspense.distance_estimated = distance
        suspense.save()
    except:
        suspense = QuotedSuspenseOrder(quoted_order = quoted_order,\
            distance_estimated = distance)
        suspense.save()
    return HttpResponse('')


@login_required
def save_distance(request):
    """
    Saves distance for general order.
    argument: Http Request
    """
    voucher_no = request.GET['voucher']
    distance = request.GET['distance']
    purchase_order_id = request.GET['order']
    purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
    financialsession = FinancialSession.objects.values('id',\
        'session_start_date', 'session_end_date')
    today = datetime.now().date()
    for value in financialsession:
        start_date = value['session_start_date']
        end_date = value['session_end_date']
        if start_date <= today <= end_date:
            session_id = value['id']
    session = FinancialSession.objects.get(pk=session_id)
    try:
        suspense = SuspenseOrder.objects.filter(voucher=voucher_no).\
            get(purchase_order=purchase_order_id)
        suspense.distance_estimated = distance
        suspense.save()
    except:
        suspense = SuspenseOrder(voucher=voucher_no,
            purchase_order=purchase_order, session_id=session,
            distance_estimated=distance)
        suspense.save()

    return HttpResponse('')


@login_required
def transport(request):
    """
    Transportation Forms.
    argument: Http Request
    returns: Render transportation form.
    """
    form = TransportForm1()
    temp = {'TransportForm':form}
    return render (request, 'suspense/transportform.html', temp)


@login_required
def sessionselect(request):
    """
    Session selection method.
    argument: Http Request
    returns: Render Transport Form with values of selected order.
    """
    if request.method == 'POST':
        form = SessionSelectForm(request.POST)
        if form.is_valid():
            session = request.POST['session'][0]
            voucher = request.POST['voucher']
            Session = FinancialSession.objects.filter(id = session).\
            values('session_start_date','session_end_date')
            for date in Session:
                session_start_date = date['session_start_date']
                session_end_date =  date['session_end_date']
            object = SuspenseOrder.objects.filter(session_id=session).\
            filter(voucher=voucher).values()
            if object:
                Transport = TransportForm1()
                messages = " Voucher "+" "+ voucher +" and Session"+" "+\
                str(session_start_date)+":"+str(session_end_date)
                request_status = request_notify()
                temp = {"TransportForm":Transport, "session":session,\
                "voucher":voucher,"messages":messages,'request':request_status}
                return render(request, 'suspense/transportform.html', temp)
            else:
                form = SessionSelectForm()
                request_status = request_notify()
                errors = "No such voucher number in selected session"
                temp = {"SelectForm":form, "errors":errors,\
                'request':request_status}
                return render(request, 'voucher/sessionselect.html', temp)
        else:
            form = SessionSelectForm(request.POST)
            request_status = request_notify()
            temp = {"SelectForm":form, 'request':request_status}
            return render(request, 'voucher/sessionselect.html', temp)
    else:
        form = SessionSelectForm()
        request_status = request_notify()
        temp = {"SelectForm":form,'request':request_status}
        return render(request, 'voucher/sessionselect.html', temp)


@login_required
def transportbill(request):
    """
    This view is used to generate the Transport Bill
    argument: Http Request
    returns: Render Transport Bill.
    """
    if request.method == 'POST':
        form = TransportForm1(request.POST)
        if form.is_valid():
            if not 'session' in request.POST:
                HttpResponseRedirect(\
                    reverse("suspense:sessionselect"))
            session = FinancialSession.objects.\
            get(id=request.POST['session'])
            session_id = FinancialSession.objects.values('id').\
            get(id=request.POST['session'])
            voucher = request.POST['voucher']
            date_of_generation = request.POST['Date_of_generation']
            vehicle = Vehicle.objects.get(id=request.POST['Vehicle'])
            kilometers_list = simplejson.dumps(\
                request.POST.getlist("kilometer"))
            kilometers = json.loads(kilometers_list)
            dated = simplejson.dumps(request.POST.getlist("date"))
            date = json.loads(dated)
            rate_object = Surcharge.objects.filter(\
                tax_name='transportation').values('value')[0]
            rate = int(rate_object['value'])
            distance = 0
            for temp_var in kilometers:
                distance = distance + int(temp_var)
            total = rate * distance
            suspense_object = SuspenseOrder.objects.filter(voucher=voucher,\
            session_id=session).update(is_cleared=0)
            try:
                if Transport.objects.filter(voucher_no=voucher, session=session).exists():
                    Transport.objects.filter(voucher_no = voucher, session=session).\
                    update(vehicle=vehicle,kilometer=kilometers ,\
                    date_of_generation=date_of_generation, total = total,\
                    date=date, rate=rate, voucher_no=voucher,\
                    session=session)
                else:
                    obj = Transport(vehicle=vehicle, kilometer=kilometers,\
                    date_of_generation=date_of_generation, total=total,\
                    date=date, rate=rate, voucher_no=voucher,\
                    session=session)
                    obj.save()
                    transport_obj = Transport.objects.filter(voucher_no=voucher,
                        session=session)[0]
                    max_id = TransportBillOfSession.objects.all().aggregate(
                        Max('id'))
                    if max_id['id__max'] == None:
                        temp_obj = TransportBillOfSession(
                            transport=transport_obj, session=session,
                            transportbillofsession=1)
                        temp_obj.save()
                    else:
                        transportbillofsession_obj = TransportBillOfSession.\
                        objects.values('transportbillofsession', 'session').\
                        get(id=max_id['id__max'])
                        if transportbillofsession_obj['session'] ==\
                        session_id['id']:
                            temp_obj = TransportBillOfSession(
                                transport=transport_obj, session=session,
                                transportbillofsession=
                                transportbillofsession_obj[
                                'transportbillofsession']+1)
                            temp_obj.save()
                        else:
                            temp_obj = TransportBillOfSession(
                                transport=transport_obj, session=session,
                                transportbillofsession=1)
                            temp_obj.save()
            except:
                pass
            temp = Transport.objects.filter(voucher_no=voucher, session=session).values()
            total_amount = Transport.objects.filter(voucher_no=voucher, session=session).\
            aggregate(Sum('total')).get('total__sum', 0.00)
            zipped_data = zip(date, kilometers)
            transport_total = []
            for date_var,kilometers_var in zipped_data:
                cal_total = rate * int(kilometers_var)
                transport_total.append(cal_total)
            zip_data = zip(date, kilometers, transport_total)
            header = HeaderFooter.objects.values('header').\
            get(is_active=True)
            footer = HeaderFooter.objects.values('footer').\
            get(is_active=True)
            request_status = request_notify()
            session_id = session.id
            return render(request, 'suspense/transport_summary.html',
                   {'words':num2eng(total_amount), 'total':total,
                   'header':header, 'kilometers':kilometers, 'rate':rate,\
                   'date':date, "voucherid":voucher, "temp":temp,\
                   'zip_data':zip_data, 'total_amount':total_amount,\
                   'date_of_generation':date_of_generation,\
                   'vehicle':vehicle,'request':request_status,\
                   'session':session_id})
        else:
            message = " Fields are mandatory"
            session = request.POST['session']
            voucher = request.POST['voucher']
            object = SuspenseOrder.objects.filter(session_id=session).\
            filter(voucher=voucher).values()
            if object:
                TransportForm = TransportForm1(request.POST)
                message = " Fields are mandatory"
                request_status = request_notify()
                temp = {"TransportForm":TransportForm, "session":session,\
                "voucher":voucher, "message":message, 'request':request_status}
                return render(request, 'suspense/transportform.html', temp)
    else:
        form = SessionSelectForm()
        request_status = request_notify()
        temp = {"SelectForm":form,'request':request_status}
        return render(request, 'voucher/sessionselect.html', temp)

@login_required
def tada_result(request):
    """
    This view is used to generate TADA bill
    argument: Http Request
    returns: Render TA/DA Form for selected order if order is valid. If order
    is not valid, it returns error on same page.
    """
    if request.method == 'POST':
        form = TaDaForm(request.POST)
        if form.is_valid():
            session = request.POST['session']
            voucher = request.POST['voucher_no']
            departure_time_from_tcc = request.POST['departure_time_from_tcc']
            arrival_time_at_site = request.POST['arrival_time_at_site']
            departure_time_from_site = request.POST['departure_time_from_site']
            arrival_time_at_tcc = request.POST['arrival_time_at_tcc']
            start_test_date = request.POST['start_test_date']
            end_test_date = request.POST['end_test_date']
            source_site = request.POST['source_site']
            testing_site = request.POST['testing_site']
            testing_staff = request.POST['testing_staff']
            testing_staff_list = testing_staff.split(',')
            list_staff = []
            if start_test_date == end_test_date:
                days = 1
            else:
                no_of_days = datetime.strptime(end_test_date, '%Y-%m-%d') -\
                datetime.strptime(start_test_date, '%Y-%m-%d')
                days = no_of_days.days + 1
            for testing_staff_var in testing_staff_list:
                testing_staff_details = Staff.objects.filter(\
                    code=testing_staff_var).values('name','daily_ta_da')
                for tada_val in testing_staff_details:
                    tada_val['daily_ta_da'] = tada_val['daily_ta_da'] * days
                list_staff.append(testing_staff_details)
            header = HeaderFooter.objects.values('header').get(is_active=True)
            footer = HeaderFooter.objects.values('footer').get(is_active=True)
            voucher_obj = VoucherId.objects.filter(session=session).\
            filter(voucher_no=voucher).\
            values_list('purchase_order_id', flat=True)
            purchase_order_var = 0
            for temp_var in voucher_obj:
                purchase_order_var = temp_var
            purchase_order_object = PurchaseOrder.objects.filter(\
                id = purchase_order_var).values('id', 'buyer_id__username',\
                'buyer_id__first_name', 'buyer_id__last_name')
            tada_total = 0
            for temp_var in list_staff:
                for tada_value in temp_var:
                    tada_total = tada_value['daily_ta_da'] + tada_total

            tada_taxes = []
            # Current valid taxes
            valid_taxes = Surcharge.objects.filter(taxes_included=1)
            tada_total_with_tax = tada_total
            for tax in valid_taxes:
                tax_name = tax.tax_name + " @ " + str(tax.value) + " %"
                tax_amount = tada_total * tax.value / 100
                tax_amount = int(round(tax_amount))
                tada_taxes.append((tax_name, tax_amount))
                tada_total_with_tax += tax_amount
            suspense_object = SuspenseOrder.objects.filter(voucher=voucher,\
                session_id=session).update(is_cleared=0)
            object = TaDa.objects.filter(session=session, voucher_no=voucher,
                start_test_date=start_test_date).values()
            if object:
                TaDa.objects.filter(session=session, voucher_no=voucher,
                start_test_date=start_test_date).update(voucher_no=voucher, session=session,\
                departure_time_from_tcc=departure_time_from_tcc,\
                arrival_time_at_site=arrival_time_at_site,\
                departure_time_from_site=departure_time_from_site,\
                arrival_time_at_tcc=arrival_time_at_tcc,\
                tada_amount=tada_total_with_tax, tada_amount_without_tax=tada_total,\
                start_test_date=start_test_date,\
                end_test_date=end_test_date, source_site=source_site,\
                testing_site=testing_site , testing_staff=testing_staff)
                tada_id = TaDa.objects.get(session=session, voucher_no=voucher, start_test_date=start_test_date).id
                tada_tax_detail = TaDa_Tax_Detail.objects.filter(tada=tada_id)
                for tax_obj, tax in zip(tada_tax_detail, tada_taxes):
                    tax_obj.name = tax[0]
                    tax_obj.amount = tax[1]
                    tax_obj.save()
            else:
                obj = TaDa(voucher_no=voucher, session=session,\
                departure_time_from_tcc=departure_time_from_tcc,\
                arrival_time_at_site=arrival_time_at_site,\
                departure_time_from_site=departure_time_from_site,\
                arrival_time_at_tcc=arrival_time_at_tcc,\
                tada_amount=tada_total_with_tax, tada_amount_without_tax=tada_total, start_test_date=start_test_date,\
                end_test_date=end_test_date, source_site=source_site,\
                testing_site=testing_site , testing_staff=testing_staff )
                obj.save()
                for tax in tada_taxes:
                    tada_tax_detail = TaDa_Tax_Detail(tada=obj, name=tax[0], amount=tax[1])
                    tada_tax_detail.save()
            recent_tada = TaDa.objects.values_list('id',flat=True).filter(voucher_no=voucher).\
                order_by('-id')[0]
            tada_obj = TaDa.objects.values('departure_time_from_tcc',\
                'arrival_time_at_site', 'departure_time_from_site',\
                'arrival_time_at_tcc', 'tada_amount', 'start_test_date',\
                'end_test_date', 'source_site', 'testing_site',\
                'date_of_generation').get(id=recent_tada)
            #tada_amount_in_words = tada_total
            tada_tax_detail_list = []
            tada_id = TaDa.objects.get(session=session, voucher_no=voucher, start_test_date=start_test_date).id
            tada_tax_detail = TaDa_Tax_Detail.objects.filter(tada=tada_id)
            for i in tada_tax_detail:
                tada_tax_detail_list.append((i.name, i.amount))
            header = HeaderFooter.objects.values('header').get(is_active=True)
            footer = HeaderFooter.objects.values('footer').get(is_active=True)
            request_status = request_notify()
            return render(request, 'suspense/tada_summary.html',{\
                'purchase_order_object':purchase_order_object,
                'tada':tada_obj, 'purchase_order_id':voucher,\
                'list_staff':list_staff, 'words':num2eng(int(tada_total_with_tax)),\
                'total':tada_total_with_tax, 'amount':tada_total, 'tax_detail': tada_tax_detail_list,\
                'request':request_status,'session':session,\
                'voucher':voucher})
        else:
            session = request.POST['session']
            voucher = request.POST['voucher_no']
            form = TaDaForm(request.POST,initial={'voucher_no':voucher,\
                'session': session})
            message = 'Fields are mandatory'
            tada = 'enable'
            request_status = request_notify()
            return render(request, 'suspense/form.html',{
                'form':form,'message':message,'request':request_status})

    else:
        if request.GET['voucher_no']:
            session = request.GET['session']
            voucher = request.GET['voucher_no']
            object = SuspenseOrder.objects.filter(session_id=session).\
            filter(voucher=voucher).values()
            if object:
                form = TaDaForm(initial={'voucher_no':voucher,\
                    'session': session})
                tada = 'enable'
                session_data = FinancialSession.objects.values(\
                    'session_start_date','session_end_date').get(id=session)
                messages = " Voucher" + " : " + voucher + " and Session" + " : " +\
                str(session_data['session_start_date']) + ":" +\
                str(session_data['session_end_date'])
                request_status = request_notify()
                return render(request, 'suspense/form.html', \
                {'form':form, 'tada':tada, 'messages':messages,\
                'request':request_status})
        else:
            return HttpResponseRedirect(\
                reverse('suspense:tada_order_session'))

@login_required
def tada_order_session(request):
    """
    This view is used to render the Allowance form.
    argument: Http Request
    returns: Render Session Select form.
    """
    if request.method == 'POST':
        form = SessionSelectForm(request.POST)
        if form.is_valid():
            session = request.POST['session']
            voucher = request.POST['voucher']
            object = SuspenseOrder.objects.filter(session_id=session).\
            filter(voucher=voucher).values()
            if object:
                form = TaDaForm(initial={'voucher_no':voucher,\
                    'session': session})
                tada = 'enable'
                session_data = FinancialSession.objects.values(\
                    'session_start_date','session_end_date').get(id=session)
                messages = " Voucher" + " : " + voucher + " and Session" + " : " +\
                str(session_data['session_start_date']) + ":" +\
                str(session_data['session_end_date'])
                request_status = request_notify()
                return render(request, 'suspense/form.html', \
                {'form':form, 'tada':tada, 'messages':messages,\
                'request':request_status})
            else:
                form = SessionSelectForm()
                request_status = request_notify()
                errors = "No such voucher number in selected session"
                temp = {"form":form , "errors":errors,'request':request_status}
                return render(request, 'suspense/form.html', temp)
        else:
            form = SessionSelectForm(request.POST)
            request_status = request_notify()
            return render(request, 'suspense/form.html', {
                'form':form, 'request':request_status})
    else:
        form = SessionSelectForm()
        request_status = request_notify()
        return render(request, 'suspense/form.html', {
            'form':form,'request':request_status})


@login_required
def mark_clear(request):
    """
    This view is used to fetch and display the data required to mark the
    suspense order as cleared.
    returns: render page with list of suspense voucher with their status and options.
    """
    if request.method == 'POST':
        date_form = DateRangeSelectionForm(request.POST)
        if date_form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            suspense_obj = SuspenseOrder.objects.filter(purchase_order__date_time__range=\
                    (start_date,end_date)).\
            values('voucher','session_id')
            suspense_cleared = SuspenseOrder.objects.filter(purchase_order__date_time__range=\
                    (start_date,end_date)).values(\
                'voucher','session_id','is_cleared')
            list_clearance = []
            list_user = []
            list_details = []
            for suspense_var in suspense_obj:
                SuspenseClearance_object = SuspenseClearance.objects.\
                filter(session = suspense_var['session_id']).\
                filter(voucher_no=suspense_var['voucher']).values('session',\
                    'voucher_no', 'lab_testing_staff','field_testing_staff',\
                    'test_date','clear_date')
                if SuspenseClearance_object:
                    list_clearance.append(SuspenseClearance_object)
            for temp_var in list_clearance:
                for voucher_var in temp_var:
                    voucher_object = VoucherId.objects.\
                    filter(voucher_no=voucher_var['voucher_no']).\
                    filter(session_id=voucher_var['session']).\
                    values('purchase_order__buyer__first_name',\
                        'purchase_order__buyer__last_name',\
                        'purchase_order__buyer__customer__address__street_address',\
                        'purchase_order__buyer__customer__address__district',\
                        'purchase_order__buyer__customer__address__province')
                    if voucher_object:
                        list_user.append(voucher_object)
            list_user_clr = zip (list_user,list_clearance)
            for suspense_var,voucher_var in list_user_clr:
                final_list = zip(suspense_var,voucher_var)
                list_details.append(final_list)
            request_status = request_notify()
            return render(request, 'suspense/mark_suspense_clear.html', {
                'listed':list_details, 'suspense_cleared':suspense_cleared,\
                'request':request_status})

    else:
        form = DateRangeSelectionForm()
        return render(request, 'suspense/form.html',{'form':form})


@login_required
def mark_status(request):
    """
    This view updates the status of given order as cleared.
    argument: Http Request
    """
    voucher = request.GET.get('voucher_no')
    session = request.GET.get('session')
    try:
        est_transport = SuspenseOrder.objects.values('distance_estimated').\
        get(voucher=voucher, session_id_id=session)
        delivery_rate = Surcharge.objects.values('value').\
        filter(tax_name = 'Transportation')[0]
        est_transport_total = est_transport['distance_estimated'] *\
        delivery_rate['value']
    except:
        est_transport_total = 0
    try:
        transport = Transport.objects.values('total').get(voucher_no=voucher,\
            session_id=session)
        transport_total = transport['total']
    except:
        transport_total = 0
    suspenseclearance = SuspenseClearance.objects.values('labour_charge',\
        'car_taxi_charge','boring_charge_internal','boring_charge_external').\
    get(voucher_no=voucher, session_id=session)
    other_charges = transport_total + suspenseclearance['labour_charge'] +\
    suspenseclearance['car_taxi_charge'] +\
    suspenseclearance['boring_charge_external']
    boring_charge_internal = suspenseclearance['boring_charge_internal']
    try:
        tada = TaDa.objects.values_list('tada_amount',flat=True).filter(voucher_no=voucher,\
            session=session)
        tada_amount = 0
        for value in tada:
            tada_amount = tada_amount + value
    except:
        tada_amount = 0
    calculate_distribution = VoucherTotal.objects.values('total').\
    get(voucher_no=voucher, session_id=session)
    suspense_total = calculate_distribution['total'] + est_transport_total
    distribution_total = suspense_total - boring_charge_internal -\
    other_charges - tada_amount
    voucherid = VoucherId.objects.values('ratio', 'college_income',\
        'admin_charges', 'purchased_item__item__category__parent__name').\
    filter(voucher_no=voucher, session_id=session)[0]
    temp_val = voucherid['purchased_item__item__category__parent__name'].split(':')
    try:
        if temp_val[1].upper() == 'FIELD WORK' or \
            temp_val[1].upper() == ' FIELD WORK':
            work_charge = round((2 * distribution_total) / 100)
        else:
            work_charge = 0
    except:
        work_charge = 0
    college_income = round((voucherid['college_income'] * distribution_total) / 100)
    admin_charges = round((voucherid['admin_charges'] * distribution_total) / 100)
    remain_cost = distribution_total - work_charge - college_income -\
    admin_charges
    split = voucherid['ratio'].split(':')
    consultancy_asset = round((remain_cost * int(split[0]))/100)
    development_fund = round((remain_cost * int(split[1]))/100)
    calculate_distribution_total = college_income + admin_charges +\
    consultancy_asset + development_fund
    CalculateDistribution.objects.filter(voucher_no=voucher,\
        session_id=session).update(college_income_calculated=college_income,\
        admin_charges_calculated=admin_charges,\
        consultancy_asset=consultancy_asset, development_fund=development_fund,\
        total=calculate_distribution_total)
    SuspenseClearance.objects.filter(voucher_no=voucher, session_id=session).\
    update(work_charge=work_charge)
    suspense_order_obj = SuspenseOrder.objects.filter(voucher=voucher).\
    filter(session_id=session).update(is_cleared='1')
    if SuspenseClearedRegister.objects.filter(voucher_no=voucher, session=session).exists():
        pass
    else:
        financialsession = FinancialSession.objects.get(id=session)
        session_id = FinancialSession.objects.values('id').get(id=session)
        max_id = SuspenseClearedRegister.objects.all().aggregate(
            Max('id'))
        if max_id['id__max'] == None:
            temp_obj = SuspenseClearedRegister(
                suspenseclearednumber=1, session=financialsession,
                voucher_no=voucher)
            temp_obj.save()
        else:
            suspenseclearednumber_obj = SuspenseClearedRegister.\
            objects.values('suspenseclearednumber', 'session').\
            get(id=max_id['id__max'])
            if suspenseclearednumber_obj['session'] == session_id['id']:
                temp_obj = SuspenseClearedRegister(
                    session=financialsession, voucher_no=voucher,
                    suspenseclearednumber=suspenseclearednumber_obj[\
                    'suspenseclearednumber']+1)
                temp_obj.save()
            else:
                clearednumber = SuspenseClearedRegister.\
                objects.filter(session_id=session).\
                aggregate(Max('suspenseclearednumber'))
                if clearednumber['suspenseclearednumber__max'] == None:
                    temp_obj = SuspenseClearedRegister(
                    suspenseclearednumber=1,\
                    session=financialsession, voucher_no=voucher)
                    temp_obj.save()
                else:
                    temp_obj = SuspenseClearedRegister(
                    suspenseclearednumber=clearednumber['suspenseclearednumber__max']+1,\
                    session=financialsession, voucher_no=voucher)
                    temp_obj.save()

    return HttpResponse("")


@login_required
def clearance_options(request):
    """
    Clearance options.
    argument: Http Request
    returns: Render page with clearance options.
    """
    voucher_no = request.GET.get('voucher_no')
    session_id = request.GET.get('session')
    financialsession = FinancialSession.objects.values('session_start_date',\
        'session_end_date').get(id=session_id)
    voucherid = VoucherId.objects.values('purchase_order_of_session',\
        'purchase_order').filter(voucher_no=voucher_no, session_id=session_id)[0]
    with_transport = 0
    try:
        Transport.objects.get(voucher_no=voucher_no, session_id=session_id)
    except:
        with_transport = 1
    details = PurchaseOrder.objects.values('buyer__first_name',\
        'buyer__last_name','buyer__customer__address__street_address',\
        'buyer__customer__title','buyer__customer__address__district',\
        'mode_of_payment__method','cheque_dd_number',\
        'cheque_dd_date').filter(id=voucherid['purchase_order'])[0]
    request_status = request_notify()
    return render(request,'suspense/clearance_options.html',\
        {'details': details,'order_id':voucherid['purchase_order_of_session'],
        'request':request_status, 'voucher_no':voucher_no,\
        'session_id':session_id, 'financialsession':financialsession,\
        'request':request_status, 'with_transport':with_transport})

def summary_page(request):
    """
    View to handle summary page.
    """
    session = request.GET['session']
    voucher = request.GET['voucher_no']
    try:
        tada = TaDa.objects.values_list('tada_amount',flat=True).filter(voucher_no=voucher,\
            session=session)
        tada_amount = 0
        for value in tada:
            tada_amount = tada_amount + value
    except:
        tada_amount = 0
    transport = Transport.objects.values('rate','total').filter(voucher_no=voucher).\
        filter(session=session)[0]
    distance_travelled = transport['total'] / transport['rate']
    other_charges = SuspenseClearance.objects.filter(voucher_no = voucher).\
        filter(session=session).values()[0]
    temp = Context({'tada':tada_amount,'distance_travelled':distance_travelled,
        'other_charge':other_charges,'rate':transport['rate']})
    content = get_template('suspense/summary.html')
    html_content = content.render(temp)
    return HttpResponse(html_content)


def transport_bill(request):
    """
    This view generate the transport bill
    Argument: Http Request.
    returns: Render transport bill fo selected bill.
    """
    if request.method == 'POST':
        session = request.POST['session']
        voucher = request.POST['voucher']
        bill_no = TransportBillOfSession.objects.values(
            'transportbillofsession').get(transport__voucher_no=voucher,
            transport__session=session)
        transport_object = Transport.objects.\
        filter(session_id = session,voucher_no = voucher).\
        values('vehicle_id__vehicle_no','kilometer',\
        'rate','date_of_generation','date','total')
        list_of_kilometer = []
        list_of_date = []
        total_list = []
        for value in transport_object:
            vehicle = value['vehicle_id__vehicle_no']
            rate = int(value['rate'])
            date_of_generation = value['date_of_generation']
            kilometer = str(value['kilometer'])[1:-1].encode("ascii",'ignore')
            kilometer_var = kilometer.split(',')
            for temp_var in kilometer_var:
                temp_value = temp_var.replace("u'","")
                temp_value = temp_value.replace("'","")
                list_of_kilometer.append(temp_value)
            date  = str(value['date'])[1:-1]
            date_var = date.split(',')
            for temp_var in date_var:
                temp_value = temp_var.replace("u'","")
                temp_value = temp_value.replace("'","")
                list_of_date.append(temp_value)
            distance = 0
            for temp_var in list_of_kilometer:
                total = rate * int(temp_var)
                total_list.append(int(total))
            total_amount = value['total']
        zip_data = zip(list_of_date,list_of_kilometer,total_list)
        client_address = VoucherId.objects.\
        filter(session_id = session,voucher_no = voucher).\
        values('purchase_order__buyer__customer__address__street_address',\
            'purchase_order__buyer__first_name',\
            'purchase_order__buyer__last_name',\
            'purchase_order__buyer__customer__title',\
            'purchase_order__buyer__customer__address__district')[0]
        header = HeaderFooter.objects.values('header').get(is_active=True)
        request_status = request_notify()
        return render(request, 'suspense/transport_bill.html',
               {'words':num2eng(total_amount), 'total':total, 'rate':rate,\
               'date':date, "bill_no":bill_no,\
               'total_amount':total_amount,'zip_data':zip_data,\
               'date_of_generation':date_of_generation,\
               'vehicle':vehicle,'request':request_status,'header':header,\
               'client_address':client_address})


def tada_bill_list(request):
    session = request.POST['session']
    voucher = request.POST['voucher']
    tada = TaDa.objects.values('id','tada_amount','start_test_date',
        'end_test_date').filter(voucher_no=voucher).filter(session=session)
    return render(request, 'suspense/tada_bill_list.html',{'tada':tada})

def tada_bill(request):
    """
    This view generate the T.A/D.A bill.
    argument: Http Request
    return: Render TA/DA bill for selected order.
    """
    tada_id = request.GET['tada_id']
    tada_obj = TaDa.objects.get(id=tada_id)
    tada_object = TaDa.objects.values\
    ('date_of_generation','departure_time_from_tcc',\
    'departure_time_from_site','arrival_time_at_tcc',\
    'arrival_time_at_site','tada_amount','start_test_date','end_test_date',\
    'source_site','testing_site','testing_staff','tada_amount_without_tax').\
    get(id=tada_id)
    start_test_date = tada_object['start_test_date']
    tada_amount = tada_object['tada_amount']
    tada_amount_without_tax = tada_object['tada_amount_without_tax']
    end_test_date = tada_object['end_test_date']
    testing_staff = tada_object['testing_staff']
    testing_staff_list = testing_staff.split(',')
    list_staff = []
    if start_test_date == end_test_date:
        days = 1
    else:
        no_of_days = (end_test_date - start_test_date).days
        days = no_of_days + 1
    for testing_staff_var in testing_staff_list:
        testing_staff_details = Staff.objects.filter(\
            code=testing_staff_var).values('name','daily_ta_da')
        for tada_val in testing_staff_details:
            tada_val['daily_ta_da'] = tada_val['daily_ta_da'] * days
        list_staff.append(testing_staff_details)
    tada_tax_detail_list = []
    tada_tax_detail = TaDa_Tax_Detail.objects.filter(tada=tada_id)
    for i in tada_tax_detail:
        tada_tax_detail_list.append((i.name, i.amount))

    voucher_obj = VoucherId.objects.values('purchase_order_of_session', 'receipt_date').\
    filter(session=tada_obj.session,voucher_no=tada_obj.voucher_no)[0]
    purchase_order_var = 0
    purchase_order_var = voucher_obj['purchase_order_of_session']
    purchase_order_object = PurchaseOrder.objects.\
    filter(voucherid__purchase_order_of_session = purchase_order_var, voucherid__session_id=tada_obj.session).values(\
        'buyer_id__first_name', 'buyer_id__last_name','buyer__customer__title',
        'buyer__customer__address__district', 'buyer__customer__address__street_address',
        'buyer__customer__address__pin', 'buyer__customer__address__province')[0]
    header = HeaderFooter.objects.values('header').get(is_active=True)
    request_status = request_notify()
    return render(request, 'suspense/tada_result.html',{\
    'purchase_order_object':purchase_order_object,
    'tada':tada_object, 'purchase_order_id':purchase_order_var,\
    'words':num2eng(int(tada_amount)),'tada_total':tada_amount,\
    'tada_amount':tada_amount_without_tax, 'tax_detail':tada_tax_detail_list,\
    'request':request_status,'session':tada_obj.session,\
    'voucher':tada_obj.voucher_no,'list_staff':list_staff,'header':header,
    'date':voucher_obj['receipt_date']
    })


def car_taxi_advance_form(request):
    if request.method == 'POST':
        sessiondata = SessionSelectForm(request.POST)
        if sessiondata.is_valid():
            voucher = sessiondata.data['voucher']
            session = sessiondata.data['session']
            object = SuspenseOrder.objects.filter(session_id=session).\
            filter(voucher=voucher).values()
            if object:
                form = CarTaxiAdvance_form(initial={'voucher_no':voucher,\
                'session':session})
                car_taxi_advance = 'enable'
                request_status = request_notify()
                return render(request, 'suspense/car_taxi_advance_form.html', \
                    {'form':form, 'request':request_status,
                    'car_taxi_advance':car_taxi_advance})
            else:
                form = SessionSelectForm()
                errors = "No such voucher number in selected session"
                request_status = request_notify()
                temp = {"form":form , "message":errors,\
                'request':request_status}
                return render(request, 'suspense/car_taxi_advance_form.html', temp)
        else:
            form = SessionSelectForm(request.POST)
            request_status = request_notify()
            return render(request, 'suspense/car_taxi_advance_form.html',\
                {'form':form, 'request':request_status})
    else:
        form = SessionSelectForm()
        request_status = request_notify()
        return render(request, 'suspense/car_taxi_advance_form.html',\
            {'form':form, 'request':request_status})


def car_taxi_advance(request):
    if request.method == 'POST':
        car_taxi_advance_form = CarTaxiAdvance_form(request.POST)
        if car_taxi_advance_form.is_valid():
            voucher = car_taxi_advance_form.data['voucher_no']
            session = car_taxi_advance_form.data['session']
            spent = car_taxi_advance_form.data['spent']
            advance = car_taxi_advance_form.data['advance']
            receipt = car_taxi_advance_form.data['receipt_no']
            receipt_session = car_taxi_advance_form.data['receipt_session']
            balance = int(advance) - int(spent)
            session_obj = FinancialSession.objects.get(pk=session)
            car_taxi_advance_obj = CarTaxiAdvance.objects.filter(
                voucher_no=voucher, session=session)
            if car_taxi_advance_obj:
                CarTaxiAdvance.objects.filter(voucher_no=voucher, session=session).\
                update(balance=balance ,spent=spent, advance=advance, receipt_no=receipt,
                    receipt_session=receipt_session)
            else:
                obj = CarTaxiAdvance(voucher_no=voucher, session=session_obj,
                    balance=balance ,spent=spent, advance=advance,
                    receipt_no=receipt, receipt_session=receipt_session)
                obj.save()
            request_status = request_notify()
            return render(request, 'suspense/car_taxi_advance_success.html',\
                {'request':request_status})
        else:
            form = CarTaxiAdvance_form(request.POST)
            request_status = request_notify()
            return render(request, 'suspense/car_taxi_advance_form.html',\
                {'form':form, 'request':request_status})
    else:
        return HttpResponseRedirect(\
            reverse("suspense:car_taxi_advance_form"))
