from django.shortcuts import render
from django.db.models import Sum, Max
from models import SuspenseClearance
from models import TaDa
from django.http import  HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse

from librehatti.catalog.models import Product
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import Surcharge
from librehatti.catalog.models import HeaderFooter

from librehatti.suspense.models import SuspenseClearance
from librehatti.suspense.models import SuspenseOrder
from librehatti.suspense.models import Transport
from librehatti.suspense.models import Vehicle
from librehatti.suspense.models import Staff
from librehatti.suspense.forms import Clearance_form
from librehatti.suspense.forms import SuspenseForm
from librehatti.suspense.forms import QuotedSuspenseForm
from librehatti.suspense.forms import TaDaForm
from librehatti.suspense.forms import TaDaSearch
from librehatti.suspense.forms import SessionSelectForm
from librehatti.suspense.forms import TransportForm1
from librehatti.prints.helper import num2eng

from librehatti.voucher.models import VoucherId, Distribution
from librehatti.voucher.models import FinancialSession, CalculateDistribution
from django.contrib.auth.decorators import login_required
import datetime
import simplejson
import json 
from datetime import date, datetime


@login_required
def add_distance(request):
    old_post = request.session.get('old_post')
    purchase_order_id = request.session.get('purchase_order_id')
    items = []
    parents = []
    field_work = []
    suspense = 0
    for id in range(0,10):
        try:
            items.append(old_post['purchaseditem_set-' + str(id) + '-item'])
        except:
            pass
  
    for item in items:
        if item:
            parents.append(PurchasedItem.objects.values(
              'item__category__parent__name','id').filter(item = item).\
              filter(purchase_order = purchase_order_id))
    
    for parent in parents:
        for category in parent:
            value = category['item__category__parent__name']
            key = category['id']
            if value.split(':')[1].upper() == 'FIELD WORK' or \
                value.split(':')[1].upper() == ' FIELD WORK':
                field_work.append(key)
   
    if field_work:
        if request.method == 'POST':
            request.session['old_post'] = old_post
            request.session['purchase_order_id'] = purchase_order_id
            return HttpResponseRedirect('/catalog/bill_cal/')
        else:
            purchase_order = PurchaseOrder.objects.values('date_time').\
                get(id = purchase_order_id)
            purchase_order_date = purchase_order['date_time'].date()
            financialsession = FinancialSession.objects.\
                values('id','session_start_date','session_end_date')
            
            for value in financialsession:
                start_date = value['session_start_date']
                end_date = value['session_end_date']
                if start_date <= purchase_order_date <= end_date:
                    session_id = value['id']

            voucher = VoucherId.objects.values('voucher_no',
                'purchased_item__item__category__name').\
                filter(purchased_item__in = field_work).\
                filter(session = session_id)
            
            return render(request,'suspense/add_distance.html',{'voucher':voucher,
                'purchase_order_id': purchase_order_id})
    elif old_post['mode_of_payment'] != '1':

        purchase_order = PurchaseOrder.objects.values('date_time').\
            get(id = purchase_order_id)
        purchase_order_date = purchase_order['date_time'].date()
        financialsession = FinancialSession.objects.\
            values('id','session_start_date','session_end_date')
        
        for value in financialsession:
            start_date = value['session_start_date']
            end_date = value['session_end_date']
            if start_date <= purchase_order_date <= end_date:
                session_id = value['id']

        session = FinancialSession.objects.get(pk = session_id)
        
        voucher = VoucherId.objects.values('voucher_no').\
            filter(purchase_order = purchase_order_id)
        order = PurchaseOrder.objects.get(pk = purchase_order_id)
        for voucher_no in voucher:
            suspense = SuspenseOrder(voucher = voucher_no['voucher_no'], 
            purchase_order = order, session_id = session, 
            distance_estimated = 0)
            suspense.save()
        request.session['old_post'] = old_post
        request.session['purchase_order_id'] = purchase_order_id
        return HttpResponseRedirect('/catalog/bill_cal/')

    else:
        request.session['old_post'] = old_post
        request.session['purchase_order_id'] = purchase_order_id
        return HttpResponseRedirect('/catalog/bill_cal/')

@login_required
def clearance_search(request):
    if request.method == 'POST':
        sessiondata = SessionSelectForm(request.POST)
        voucher = sessiondata.data['voucher']
        session = sessiondata.data['session']
        object = SuspenseOrder.objects.filter(session_id = session).\
        filter(voucher = voucher).values()
        if object:
            try:
                transport = Transport.objects.values('total').\
                get(voucher_no = voucher, session = session)
                form = Clearance_form(initial={'voucher_no': voucher,\
                'session': session, 'car_taxi_charge':transport['total']})
                clearance = 'enable'
                return render(request, 'suspense/suspense_first.html', \
                    {'form':form,'clearance':clearance})
            except:
                form = SessionSelectForm()
                errors = "No such voucher number in Transport" 
                temp = {"SelectForm" : form , "errors" : errors}
                return render(request, 'voucher/clsessionselect.html', temp) 
        else:
                form = SessionSelectForm()
                errors = "No such voucher number in selected session" 
                temp = {"SelectForm" : form , "errors" : errors}
                return render(request, 'voucher/clsessionselect.html', temp) 
    else:
        form = SessionSelectForm()
        return render(request, 'suspense/suspense_first.html', \
            {'form':form}) 


@login_required
def clearance(request):
    if 'Search' in request.GET:
        ref_no = request.GET['ref_no']
        cl_report = Clearance_form(initial = {'work_charge':0, 'labour_charge':
                    0, 'car_taxi_charge':0,'boring_charge_external':0,
                    'boring_charge_internal':0,'Test_date':datetime.date.today
                     })
        temp = {'ref_no':ref_no,'cl_report':cl_report,}
        return render(request, 'suspense/suspenseform.html',temp)


@login_required
def clearance_result(request):
    if request.method == 'POST':
        form = Clearance_form(request.POST)
        if form.is_valid():
            formdata = form.cleaned_data
            voucher_no = formdata['voucher_no']
            session = formdata['session']
            work_charge = formdata['work_charge']
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
            try:
                SuspenseClearance.objects.get(voucher_no=voucher_no, session=financialsession['id'])
                SuspenseClearance.objects.\
                filter(voucher_no=voucher_no, session=financialsession['id']).\
                update(session=session,voucher_no=voucher_no, work_charge=work_charge,\
                    labour_charge=labour_charge, car_taxi_charge=car_taxi_charge,\
                    boring_charge_external=boring_charge_external,\
                    boring_charge_internal=boring_charge_internal,\
                    lab_testing_staff=lab_testing_staff,\
                    field_testing_staff=field_testing_staff,\
                    test_date=test_date)
            except:
                obj= SuspenseClearance(session=session,voucher_no=voucher_no,
                     work_charge=work_charge,labour_charge=labour_charge,
                     car_taxi_charge=car_taxi_charge, 
                     boring_charge_external=boring_charge_external,
                     boring_charge_internal=boring_charge_internal,lab_testing_staff=
                     lab_testing_staff,field_testing_staff=field_testing_staff,
                     test_date=test_date)
                obj.save()
            temp = {'session':session,'voucher_no': voucher_no,\
                    'work_charge':work_charge ,'labour_charge':
                    labour_charge, 'car_taxi_charge':car_taxi_charge,
                    'boring_charge_external':boring_charge_external,
                    'boring_charge_internal':boring_charge_internal,
                    'lab_testing_staff':lab_testing_staff, 'field_testing_staff':
                    field_testing_staff, 'test_date':test_date,\
                    'clear_date':clear_date}
            return render(request, 'suspense/clearance_result.html', temp)
        else:
            return HttpResponse('Form is not valid. Please enter all field')
    else:
        return HttpResponseRedirect(reverse('librehatti.suspense.views.clearance_search'))


@login_required
def with_transport(request):
    number = request.GET['voucher_no']
    session = request.GET['session']
    split = session.split(' : ')
    start_date = datetime.strptime(split[0], '%Y-%m-%d').date()
    end_date = datetime.strptime(split[1], '%Y-%m-%d').date()
    financialsession = FinancialSession.objects.values('id').\
    get(session_start_date=start_date, session_end_date=end_date)
    suspenseclearance = SuspenseClearance.objects.values('work_charge',\
    'labour_charge','car_taxi_charge','boring_charge_internal',\
    'boring_charge_external','lab_testing_staff','field_testing_staff',\
    'test_date','clear_date').\
    get(voucher_no=number, session=financialsession['id'])
    othercharge = suspenseclearance['labour_charge'] + suspenseclearance['car_taxi_charge']
    lab_staff_list = suspenseclearance['lab_testing_staff'].split(',')
    lab_staff_name_list = Staff.objects.values('name','position').filter(code__in=lab_staff_list)
    staff = Staff.objects.filter(code__in=lab_staff_list).aggregate(Sum('daily_ta_da'))
    field_staff_list = suspenseclearance['field_testing_staff'].split(',')
    field_staff_name_list = Staff.objects.values('name','position').filter(code__in=field_staff_list)
    staff_obj = Staff.objects.filter(code__in=field_staff_list).aggregate(Sum('daily_ta_da'))
    ta_da_total = staff['daily_ta_da__sum'] + staff_obj['daily_ta_da__sum']
    voucherid = VoucherId.objects.values('ratio','purchase_order',\
    'purchase_order__date_time','purchase_order__buyer__first_name',\
    'purchase_order__buyer__last_name',\
    'purchase_order__buyer__customer__address__street_address',\
    'purchase_order__buyer__customer__address__city',\
    'purchase_order__buyer__customer__address__pin',\
    'purchase_order__buyer__customer__address__province','college_income',\
    'admin_charges').get(voucher_no=number, session=financialsession['id'])
    distribution = Distribution.objects.values('name').\
    get(ratio=voucherid['ratio'])
    calculate_distribution = CalculateDistribution.objects.\
    values('college_income_calculated','admin_charges_calculated',\
    'consultancy_asset','development_fund','total').\
    get(voucher_no=number, session=financialsession['id'])
    if suspenseclearance['boring_charge_external'] !=0:
        total = calculate_distribution['total'] + othercharge + ta_da_total +\
        suspenseclearance['work_charge'] +\
        suspenseclearance['boring_charge_internal'] +\
        suspenseclearance['boring_charge_external']
        total_in_words = num2eng(total)
        rowspan = 10
    else:
        total = calculate_distribution['total'] + othercharge + ta_da_total +\
        suspenseclearance['work_charge'] + suspenseclearance['boring_charge_internal']
        total_in_words = num2eng(total)
        rowspan = 9
    header = HeaderFooter.objects.values('header').get(is_active=True)
    footer = HeaderFooter.objects.values('footer').get(is_active=True)
    return render(request,'suspense/with_transport.html', {'header':header,\
                'footer':footer, 'voucher_no':number,\
                'date':suspenseclearance['clear_date'],\
                'calculate_distribution':calculate_distribution,\
                'suspense_clearance':suspenseclearance,\
                'field_staff':field_staff_name_list,\
                'lab_staff':lab_staff_name_list, 'ratio':voucherid['ratio'],\
                'distribution':distribution['name'],\
                'purchase_order':voucherid['purchase_order'],\
                'order_date':voucherid['purchase_order__date_time'].date(),\
                'address':voucherid, 'ta_da':ta_da_total,\
                'othercharge':othercharge, 'total':total,\
                'total_in_words':total_in_words,\
                'test_date':suspenseclearance['test_date'],\
                'charges':voucherid, 'rowspan':rowspan})


@login_required
def withouttransport(request):
    number = request.GET['voucher_no']
    session = request.GET['session']
    split = session.split(' : ')
    start_date = datetime.strptime(split[0], '%Y-%m-%d').date()
    end_date = datetime.strptime(split[1], '%Y-%m-%d').date()
    financialsession = FinancialSession.objects.values('id').\
    get(session_start_date=start_date, session_end_date=end_date)
    suspenseclearance = SuspenseClearance.objects.values('work_charge','labour_charge',\
    'boring_charge_internal','boring_charge_external','field_testing_staff',\
    'lab_testing_staff','test_date','clear_date').\
    get(voucher_no=number, session=financialsession['id'])
    othercharge = suspenseclearance['labour_charge']
    lab_staff_list = suspenseclearance['lab_testing_staff'].split(',')
    lab_staff_name_list = Staff.objects.values('name','position').filter(code__in=lab_staff_list)
    staff = Staff.objects.filter(code__in=lab_staff_list).aggregate(Sum('daily_ta_da'))
    field_staff_list = suspenseclearance['field_testing_staff'].split(',')
    field_staff_name_list = Staff.objects.values('name','position').filter(code__in=field_staff_list)
    staff_obj = Staff.objects.filter(code__in=field_staff_list).aggregate(Sum('daily_ta_da'))
    ta_da_total = staff['daily_ta_da__sum'] + staff_obj['daily_ta_da__sum']
    voucherid = VoucherId.objects.values('ratio','purchase_order',\
    'purchase_order__date_time','purchase_order__buyer__first_name',\
    'purchase_order__buyer__last_name',\
    'purchase_order__buyer__customer__address__street_address',\
    'purchase_order__buyer__customer__address__city',\
    'purchase_order__buyer__customer__address__pin',\
    'purchase_order__buyer__customer__address__province','college_income',\
    'admin_charges').get(voucher_no=number, session=financialsession['id'])
    distribution = Distribution.objects.values('name').\
    get(ratio=voucherid['ratio'])
    calculate_distribution = CalculateDistribution.objects.\
    values('college_income_calculated','admin_charges_calculated',\
    'consultancy_asset','development_fund','total').\
    get(voucher_no=number, session=financialsession['id'])
    if suspenseclearance['boring_charge_external'] !=0:
        total = calculate_distribution['total'] + othercharge + ta_da_total +\
        suspenseclearance['work_charge'] + \
        suspenseclearance['boring_charge_internal'] +\
        suspenseclearance['boring_charge_external']
        total_in_words = num2eng(total)
        rowspan = 10
    else:
        total = calculate_distribution['total'] + othercharge + ta_da_total +\
        suspenseclearance['work_charge'] + suspenseclearance['boring_charge_internal']
        total_in_words = num2eng(total)
        rowspan = 9
    header = HeaderFooter.objects.values('header').get(is_active=True)
    footer = HeaderFooter.objects.values('footer').get(is_active=True)
    return render(request,'suspense/withouttransport.html', {'header':header,\
                'footer':footer, 'voucher_no':number,\
                'date':suspenseclearance['clear_date'],\
                'calculate_distribution':calculate_distribution,\
                'suspense_clearance':suspenseclearance,\
                'field_staff':field_staff_name_list,\
                'lab_staff':lab_staff_name_list, 'ratio':voucherid['ratio'],\
                'distribution':distribution['name'],\
                'purchase_order':voucherid['purchase_order'],\
                'order_date':voucherid['purchase_order__date_time'].date(),\
                'address':voucherid,'othercharge':othercharge ,'ta_da':ta_da_total,\
                'total':total,'total_in_words':total_in_words,\
                'test_date':suspenseclearance['test_date'],'charges':voucherid,\
                'rowspan':rowspan})



@login_required
def wtransport(request):
    number = request.GET['voucher_no']
    session = request.GET['session']
    split = session.split(' : ')
    start_date = datetime.strptime(split[0], '%Y-%m-%d').date()
    end_date = datetime.strptime(split[1], '%Y-%m-%d').date()
    financialsession = FinancialSession.objects.values('id').\
    get(session_start_date=start_date, session_end_date=end_date)
    suspenseclearance = SuspenseClearance.objects.values('work_charge',\
    'boring_charge_internal','field_testing_staff','lab_testing_staff','test_date','clear_date').\
    get(voucher_no=number, session=financialsession['id'])
    lab_staff_list = suspenseclearance['lab_testing_staff'].split(',')
    lab_staff_name_list = Staff.objects.values('name','position').filter(code__in=lab_staff_list)
    field_staff_list = suspenseclearance['field_testing_staff'].split(',')
    field_staff_name_list = Staff.objects.values('name','position').filter(code__in=field_staff_list)
    voucherid = VoucherId.objects.values('ratio','purchase_order',\
    'purchase_order__date_time','purchase_order__buyer__first_name',\
    'purchase_order__buyer__last_name',\
    'purchase_order__buyer__customer__address__street_address',\
    'purchase_order__buyer__customer__address__city',\
    'purchase_order__buyer__customer__address__pin',\
    'purchase_order__buyer__customer__address__province','college_income',\
    'admin_charges').get(voucher_no=number, session=financialsession['id'])
    distribution = Distribution.objects.values('name').\
    get(ratio=voucherid['ratio'])
    calculate_distribution = CalculateDistribution.objects.\
    values('college_income_calculated','admin_charges_calculated',\
    'consultancy_asset','development_fund','total').\
    get(voucher_no=number, session=financialsession['id'])
    total_in_words = num2eng(calculate_distribution['total'])
    header = HeaderFooter.objects.values('header').get(is_active=True)
    footer = HeaderFooter.objects.values('footer').get(is_active=True)
    return render(request,'suspense/wtransport.html', {'header':header,\
                'footer':footer, 'voucher_no':number,\
                'date':suspenseclearance['clear_date'],\
                'calculate_distribution':calculate_distribution,\
                'suspense_clearance':suspenseclearance,\
                'field_staff':field_staff_name_list,\
                'lab_staff':lab_staff_name_list, 'ratio':voucherid['ratio'],\
                'distribution':distribution['name'],\
                'purchase_order':voucherid['purchase_order'],\
                'order_date':voucherid['purchase_order__date_time'].date(),\
                'address':voucherid, 'total_in_words':total_in_words,\
                'test_date':suspenseclearance['test_date'],'charges':voucherid})


@login_required
def other_charges(request):
    number = request.GET['voucher_no']
    session = request.GET['session']
    split = session.split(' : ')
    start_date = datetime.strptime(split[0], '%Y-%m-%d').date()
    end_date = datetime.strptime(split[1], '%Y-%m-%d').date()
    financialsession = FinancialSession.objects.values('id').\
    get(session_start_date=start_date, session_end_date=end_date)
    transport = Transport.objects.values('id','date_of_generation').\
    get(voucher_no = number, session = financialsession['id'])
    suspenseclearance = SuspenseClearance.objects.values('work_charge',\
    'boring_charge_internal','boring_charge_external','labour_charge','car_taxi_charge',\
    'field_testing_staff','lab_testing_staff','clear_date').\
    get(voucher_no=number, session=financialsession['id'])
    lab_staff_list = suspenseclearance['lab_testing_staff'].split(',')
    lab_staff_name_list = Staff.objects.filter(code__in=lab_staff_list).\
    aggregate(Sum('daily_ta_da'))
    field_staff_list = suspenseclearance['field_testing_staff'].split(',')
    field_staff_name_list = Staff.objects.filter(code__in=field_staff_list).\
    aggregate(Sum('daily_ta_da'))
    ta_da_total = lab_staff_name_list['daily_ta_da__sum'] + field_staff_name_list['daily_ta_da__sum']
    voucherid = VoucherId.objects.values('ratio','purchase_order',\
    'purchase_order__date_time','purchase_order__buyer__first_name',\
    'purchase_order__buyer__last_name',\
    'purchase_order__buyer__customer__address__street_address',\
    'purchase_order__buyer__customer__address__city',\
    'purchase_order__buyer__customer__address__pin',\
    'purchase_order__buyer__customer__address__province').\
    get(voucher_no=number, session=financialsession['id'])
    if suspenseclearance['boring_charge_external'] !=0:
        boring_charges = suspenseclearance['boring_charge_internal'] +\
        suspenseclearance['boring_charge_external']
    else:
        boring_charges = suspenseclearance['boring_charge_internal']
    other_charges = boring_charges + suspenseclearance['car_taxi_charge'] +\
    suspenseclearance['labour_charge']
    total = other_charges + ta_da_total
    header = HeaderFooter.objects.values('header').get(is_active=True)
    footer = HeaderFooter.objects.values('footer').get(is_active=True)
    return render(request,'suspense/othercharge.html', {'header':header,\
                'footer':footer, 'voucher_no':number,\
                'date':suspenseclearance['clear_date'],\
                'suspense_clearance':suspenseclearance,\
                'purchase_order':voucherid['purchase_order'],\
                'order_date':voucherid['purchase_order__date_time'].date(),\
                'address':voucherid, 'ta_da':ta_da_total, 'boring_charges':boring_charges,\
                'total':total, 'other_charges':other_charges,'transport_id':transport['id'],\
                'date_of_generation':transport['date_of_generation']})


@login_required
def suspense(request):
        form = SuspenseForm()   
        return render(request,'suspense/form.html',{'form':form})


@login_required
def save_charges(request):
	if request.method=='GET':		
	    option=request.GET['Purchase_order']
	    charges=request.GET['distance']
	    obj = SuspenseOrder(purchase_order_id=option, 
                                transportation=charges)
	    obj.save()
	    return HttpResponse('Thanks!')
    


@login_required
def quoted_add_distance(request):
    old_post = request.session.get('old_post')
    quote_order_id = request.session.get('quote_order_id')
    items = []
    suspense = 0
    url = "/bills/quotation/bill/" + str(quote_order_id)
    for id in range(0,10):
        try:
            items.append(old_post['quoteditem_set-' + str(id) + '-item'])
        except:
            pass
  
    for item in items:
        if item:
            parents = Product.objects.values(
              'category__parent__name').filter(id = item)
    
    for parent in parents:
        for key, value in parent.iteritems():
            if value == 'Field Work':
                suspense = 1
                break

    if old_post['mode_of_payment'] != '1' or suspense == 1:
        if request.method == 'POST':
            form = QuotedSuspenseForm(request.POST)
            if form.is_valid:
                form.save()
                return HttpResponseRedirect(url)
        else:
            form = QuotedSuspenseForm(initial = {'quote_order':quote_order_id,
              'distance':0}) 
            return render(request,'suspense/form.html',{'form':form,'test':'test'})
    else:
        return HttpResponseRedirect(url)

@login_required
def save_distance(request):
    voucher_no = request.GET['voucher']
    distance = request.GET['distance']
    purchase_order_id = request.GET['order']
    
    purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
    financialsession = FinancialSession.objects.values('id','session_start_date',
        'session_end_date')
    today = datetime.now().date()

    for value in financialsession:
        start_date = value['session_start_date']
        end_date = value['session_end_date']
        if start_date <= today <= end_date:
            session_id = value['id']

    session = FinancialSession.objects.get(pk = session_id)

    try:
        suspense = SuspenseOrder.objects.filter(voucher = voucher_no).\
            get(purchase_order = purchase_order_id)
        suspense.distance_estimated = distance
        suspense.save()

    except:
        suspense = SuspenseOrder(voucher = voucher_no, 
            purchase_order = purchase_order, session_id = session, 
            distance_estimated = distance)
        suspense.save()

    return HttpResponse('')

@login_required
def transport(request):
    form = TransportForm1()
    temp = {'TransportForm' : form}
    return render (request, 'suspense/transportform.html', temp)

@login_required
def sessionselect(request):
    if 'button1' in request.POST:
        form = SessionSelectForm(request.POST)
        if form.is_valid():
            session = request.POST['session'][0]
            voucher = request.POST['voucher']
            object = SuspenseOrder.objects.filter(session_id = session).\
            filter(voucher = voucher).values()
            if object:
                Transport = TransportForm1()
                messages = "Transport Bill for Voucher Number"+" "+ voucher +\
                " and Session"+" "+session
                temp = {"Transport" : Transport, "session" : session,\
                "voucher" : voucher, "messages" : messages}
                return render(request, 'suspense/transportform.html', temp)
            else:
                form = SessionSelectForm()
                errors = "No such voucher number in selected session" 
                temp = {"SelectForm" : form , "errors" : errors}
                return render(request, 'voucher/sessionselect.html', temp)  
        else:
            form = SessionSelectForm()
            temp = {"SelectForm" : form}
            return render(request, 'voucher/sessionselect.html', temp)

    else:
        form = SessionSelectForm()
        temp = {"SelectForm" : form}
        return render(request, 'voucher/sessionselect.html', temp)

@login_required
def transportbill(request):
    if 'button1' in request.POST:
        form = TransportForm1(request.POST)
        if form.is_valid():
            if 'button1' in request.POST:
                if not 'session' in request.POST:
                    HttpResponseRedirect(reverse("librehatti.suspense.views.sessionselect"))
                session = FinancialSession.objects.get(id=request.POST['session'])
                voucher = request.POST['voucher']
                date_of_generation = request.POST['Date_of_generation']
                vehicle = Vehicle.objects.get(id=request.POST['Vehicle'])
                kilometers_list = simplejson.dumps(request.POST.getlist("kilometer"))
                kilometers = json.loads(kilometers_list)
                dated = simplejson.dumps(request.POST.getlist("date"))
                date = json.loads(dated)
                rate_object = Surcharge.objects.filter(tax_name= 'transportation').\
                values('value')[0]
                rate = int(rate_object['value'])
                distance = 0
                for i in kilometers:
                    distance = distance + int(i)
                total = rate * distance
                try:
                    if Transport.objects.filter(voucher_no = voucher).exists():
                        Transport.objects.filter(voucher_no = voucher).\
                        update(vehicle=vehicle,kilometer=kilometers ,\
                        date_of_generation = date_of_generation, total = total,\
                        date=date, rate=rate, voucher_no=voucher, session=session)
                    else:
                        obj = Transport(vehicle=vehicle,kilometer=kilometers ,\
                        date_of_generation = date_of_generation, total = total,\
                        date=date, rate=rate, voucher_no=voucher, session=session)
                        obj.save()
                except:
                    pass 
                temp = Transport.objects.filter(voucher_no = voucher).values()
                total_amount = Transport.objects.filter(voucher_no = voucher).\
                aggregate(Sum('total')).get('total__sum',0.00)
                zipped_data  = zip(date, kilometers) 
                a = [] 
                for i,j in  zipped_data:
                    c = rate * int(j)
                    a.append(c)
                zip_data = zip(date, kilometers, a)
                header = HeaderFooter.objects.values('header').get(is_active=True)
                footer = HeaderFooter.objects.values('footer').get(is_active=True)
                return render(request,'suspense/transport_bill.html', 
                       {'words' : num2eng(total_amount), 
                        'total' : total , 'header':header, 'footer':footer,
                        'kilometers' : kilometers, 'rate': rate, 'date': date,
                        "voucherid": voucher, "temp" : temp,
                        'zip_data': zip_data, 'total_amount': total_amount,
                        'date_of_generation' : date_of_generation,
                        'vehicle' : vehicle}) 
                         
    else:
        form = TransportForm1()
    return render(request, 'suspense/transportform.html', {'TransportForm':form}) 

@login_required
def tada_result(request):
    if request.method == 'POST':
        form = TaDaForm(request.POST)
        if form.is_valid():
            session = request.POST['session']
            voucher = request.POST['voucher_no']
            departure_time_from_tcc = request.POST['departure_time_from_tcc']
            arrival_time_at_site = request.POST['arrival_time_at_site']
            departure_time_from_site = request.POST['departure_time_from_site']
            arrival_time_at_tcc = request.POST['arrival_time_at_tcc']
            tada_amount = request.POST['tada_amount']
            start_test_date = request.POST['start_test_date']
            end_test_date = request.POST['end_test_date']
            source_site = request.POST['source_site']
            testing_site = request.POST['testing_site']
            testing_staff = request.POST['testing_staff']
            testing_staff_list = testing_staff.split(',')
            list_staff = []
            for a in testing_staff_list:
                d = Staff.objects.filter(code = a).values('name','daily_ta_da')
                g = d
                list_staff.append(d)
            header = HeaderFooter.objects.values('header').get(is_active=True)
            footer = HeaderFooter.objects.values('footer').get(is_active=True)
            voucher_obj = VoucherId.objects.filter(session = session).\
            filter(voucher_no = voucher).values_list('purchase_order_id', flat = True)
            c = 0
            for a in voucher_obj:
                c = a
            purchase_order_object = PurchaseOrder.objects.filter(id = c).\
            values('id','buyer_id__username','buyer_id__first_name','buyer_id__last_name')
            f = 0
            for var in list_staff:
                for cha in var:
                    f = cha['daily_ta_da'] + f
            if TaDa.objects.filter(voucher_no = voucher).filter(session = session).exists():
                TaDa.objects.filter(voucher_no = voucher).\
                update(voucher_no = voucher, session = session,\
                departure_time_from_tcc = departure_time_from_tcc,\
                arrival_time_at_site = arrival_time_at_site,\
                departure_time_from_site = departure_time_from_site,\
                arrival_time_at_tcc = arrival_time_at_tcc,\
                tada_amount = tada_amount, start_test_date = start_test_date,\
                end_test_date = end_test_date, source_site = source_site,\
                testing_site = testing_site , testing_staff = testing_staff,)

            else:
                obj = TaDa(voucher_no = voucher, session = session,\
                departure_time_from_tcc = departure_time_from_tcc,\
                arrival_time_at_site = arrival_time_at_site,\
                departure_time_from_site = departure_time_from_site,\
                arrival_time_at_tcc = arrival_time_at_tcc,\
                tada_amount = tada_amount, start_test_date = start_test_date,\
                end_test_date = end_test_date, source_site = source_site,\
                testing_site = testing_site , testing_staff = testing_staff )
                obj.save()
            tada_obj = TaDa.objects.values('departure_time_from_tcc',\
                'arrival_time_at_site','departure_time_from_site',\
                'arrival_time_at_tcc','tada_amount','start_test_date',\
                'end_test_date','source_site','testing_site'\
                ,'date_of_generation').get(voucher_no = voucher)
            tada_amount_in_words = tada_obj['tada_amount']
            header = HeaderFooter.objects.values('header').get(is_active=True)
            footer = HeaderFooter.objects.values('footer').get(is_active=True)
            return render(request, 'suspense/tada_result.html',{\
                'purchase_order_object':purchase_order_object,
                'tada':tada_obj,'purchase_order_id': voucher,\
                'list_staff':list_staff,'header':header,'footer':footer,
                'words' : num2eng(int(tada_amount)),'total':f })
        else:    
            form = TaDaForm()
            tada = 'enable'
            return render(request, 'suspense/form.html',{'form':form})
    else:
        return HttpResponseRedirect(reverse('librehatti.suspense.views.tada_order_session'))

@login_required
def tada_order_session(request):
    if request.method == 'POST':
        form = SessionSelectForm(request.POST)
        if form.is_valid():
            session = request.POST['session']
            voucher = request.POST['voucher']
            object = SuspenseOrder.objects.filter(session_id = session).\
            filter(voucher = voucher).values()
            if object:
                    form = TaDaForm(initial = {'voucher_no':voucher, 'session': session})
                    tada = 'enable'
                    return render(request, 'suspense/form.html', \
                    {'form':form,'tada':tada})
            else:
                form = SessionSelectForm()
                errors = "No such voucher number in selected session"
                temp = {"form" : form , "errors" : errors}
                return render(request, 'suspense/form.html',\
                temp)
        else:
            form = SessionSelectForm()
            return render(request, 'suspense/form.html', \
            {'form':form})                 
    else:
        form = SessionSelectForm()
        return render(request, 'suspense/form.html', \
            {'form':form}) 
