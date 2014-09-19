from django.shortcuts import render
from django.db.models import Sum, Max
from models import SuspenseClearance
from models import TaDa
from django.http import  HttpResponseRedirect, HttpResponse

from librehatti.catalog.models import Product
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import Surcharge

from librehatti.suspense.models import SuspenseClearance
from librehatti.suspense.models import SuspenseOrder
from librehatti.suspense.forms import Clearance_form
from librehatti.suspense.forms import SuspenseForm
from librehatti.suspense.forms import QuotedSuspenseForm
from librehatti.suspense.forms import TaDaForm
from librehatti.suspense.forms import TaDaSearch

from librehatti.prints.helper import num2eng

from librehatti.voucher.models import VoucherId
from librehatti.voucher.models import FinancialSession

import datetime


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

def clearance_search(request):
    form = TaDaSearch
    return render(request,'suspense/suspense_first.html',{
                  'search_form': form})


def clearance(request):
    if 'Search' in request.GET:
        ref_no = request.GET['ref_no']
        cl_report = Clearance_form(initial = {'work_charge':0, 'labour_charge':
                    0, 'car_taxi_charge':0,'boring_charge_external':0,
                    'boring_charge_internal':0,'Test_date':datetime.date.today
                     })
        temp = {'ref_no':ref_no,'cl_report':cl_report,}
        return render(request, 'suspense/suspenseform.html',temp)


def clearance_result(request):
    if 'Submit' in request.GET:
        ref_no = request.GET['job']       
        work_charge = request.GET['work_charge']
        labour_charge = request.GET['labour_charge']
        car_taxi_charge= request.GET['car_taxi_charge']
        boring_charge_external= request.GET['boring_charge_external']
        boring_charge_internal= request.GET['boring_charge_internal']
        lab_testing_staff=request.GET['lab_testing_staff']
        field_testing_staff= request.GET['field_testing_staff']
        Test_date= request.GET['test_date']
        obj= SuspenseClearance(suspense_id=ref_no, work_charge=work_charge,
             labour_charge=labour_charge, car_taxi_charge=car_taxi_charge, 
             boring_charge_external=boring_charge_external,
             boring_charge_internal=boring_charge_internal,lab_testing_staff=
             lab_testing_staff,field_testing_staff=field_testing_staff,
             test_date=Test_date)
        obj.save()
        temp = {'ref_no': ref_no,'work_charge':work_charge ,'labour_charge':
                labour_charge, 'car_taxi_charge':car_taxi_charge,
                'boring_charge_external':boring_charge_external,
                'boring_charge_internal':boring_charge_internal,
                'lab_testing_staff':lab_testing_staff, 'field_testing_staff':
                field_testing_staff, 'Test_date':Test_date}
        return render(request, 'suspense/clearance_result.html', temp) 


def other_charges(request):
        obj = SuspenseClearance.objects.filter(id=1).values(
              'boring_charge_external','labour_charge','car_taxi_charge')
        header = HeaderOfBills.objects.values('header').order_by('-id')[0]
        return render(request,'suspense/othercharge.html',{'obj':obj,'header':header})


def withouttransport(request):
    header = HeaderOfBills.objects.values('header').order_by('-id')[0]
    return render(request,'suspense/withouttransport.html', {'header':header})


def with_transport(request):
    header = HeaderOfBills.objects.values('header').order_by('-id')[0]
    return render(request,'suspense/with_transport.html', {'header':header})


def wtransport(request):
    header = HeaderOfBills.objects.values('header').order_by('-id')[0]
    return render(request,'suspense/wtransport.html', {'header':header})


def suspense(request):
        form = SuspenseForm()   
        return render(request,'suspense/form.html',{'form':form})


def save_charges(request):
	if request.method=='GET':		
	    option=request.GET['Purchase_order']
	    charges=request.GET['distance']
	    obj = SuspenseOrder(purchase_order_id=option, 
                                transportation=charges)
	    obj.save()
	    return HttpResponse('Thanks!')
	    
	    
def tada_search(request):
    form = TaDaSearch
    return render( request, 'suspense/tada_search.html', {
                    'search_form': form })


def tada_form(request):
    ref_no = request.GET['ref_no']
    form= TaDaForm( initial = {'suspense': ref_no } )
    return render( request, 'suspense/tada_form.html', {
                        'form' : form, 'ref_no':ref_no } ) 
    


def tada_result(request):
    if 'Submit' in request.GET:
       suspense = request.GET['suspense']
       departure_time_from_tcc = request.GET['departure_time_from_tcc']
       arrival_time_at_site = request.GET['arrival_time_at_site']
       departure_time_from_site= request.GET['departure_time_from_site']
       arrival_time_at_tcc= request.GET['arrival_time_at_tcc']
       tada_amount= request.GET['tada_amount']
       start_test_date=request.GET['start_test_date']
       end_test_date= request.GET['end_test_date']
       source_site= request.GET['source_site']
       testing_site= request.GET['testing_site']
       testing_staff= request.GET['testing_staff']
       obj= TaDa(suspense=suspense, departure_time_from_tcc =
            departure_time_from_tcc,arrival_time_at_site=arrival_time_at_site,
            departure_time_from_site=departure_time_from_site,
            arrival_time_at_tcc=arrival_time_at_tcc,tada_amount=tada_amount,
            start_test_date=start_test_date,end_test_date=end_test_date, 
            source_site=source_site, testing_site=testing_site,
            testing_staff=testing_staff )
       obj.save()
       i=TaDa.objects.all().aggregate(Max('id'))
       j=i['id__max']
       staff = testing_staff.split(",")
       total_cost = 0
       for person in staff:
         total_cost= total_cost + int(tada_amount)
       rupees_in_words = num2eng(total_cost)
       purchase_order = PurchaseOrder.objects.all()
       obj1 = TaDa.objects.filter(id=j).values('departure_time_from_tcc' ,
              'arrival_time_at_site','departure_time_from_site',
              'arrival_time_at_tcc', 'tada_amount','start_test_date',
              'end_test_date','source_site', 'testing_site','testing_staff')
       return render(request, 'suspense/tada_result.html', { 'obj':obj1, 
       'total_cost':total_cost, 'staff':staff, 'rupees_in_words':
       rupees_in_words,'purchase_order':purchase_order})

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

def save_distance(request):
    voucher_no = request.GET['voucher']
    distance = request.GET['distance']
    purchase_order_id = request.GET['order']
    
    purchase_order = PurchaseOrder.objects.get(pk=purchase_order_id)
    financialsession = FinancialSession.objects.values('id','session_start_date',
        'session_end_date')
    today = datetime.date.today()
    
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

