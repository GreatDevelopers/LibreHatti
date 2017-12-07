from django.shortcuts import render
#import inflect
from random import randint
from django.core.urlresolvers import reverse

from django.http import HttpResponse

from librehatti.reports.forms import DailyReportForm
from librehatti.reports.forms import ConsultancyFunds
from librehatti.reports.forms import DateRangeSelectionForm
from librehatti.reports.forms import MonthYearForm, AmountForm
from librehatti.reports.forms import PaidTaxesForm, LabReportForm

from datetime import datetime
import calendar

from librehatti.catalog.request_change import request_notify
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import Bill
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import Category
from librehatti.catalog.models import TaxesApplied
from librehatti.catalog.models import Surcharge
from librehatti.catalog.models import NonPaymentOrder
from librehatti.catalog.models import NonPaymentOrderOfSession
from librehatti.catalog.models import ModeOfPayment

from librehatti.suspense.models import SuspenseOrder
from librehatti.suspense.models import Transport
from librehatti.suspense.models import TaDa, Staff
from librehatti.suspense.models import SuspenseClearance
from librehatti.suspense.models import SuspenseClearedRegister

from librehatti.voucher.models import CalculateDistribution
from librehatti.voucher.models import VoucherId, VoucherTotal
from librehatti.voucher.models import Distribution

from librehatti.bills.models import QuotedOrder
from librehatti.bills.models import QuotedOrderofSession
from librehatti.bills.models import QuotedTaxesApplied
from librehatti.bills.models import QuotedItem

from useraccounts.models import User

from django.db.models import Sum

from django.contrib.auth.decorators import login_required


@login_required
def daily_report_result(request):
    """
    This view is used to display the daily report registers
    Argument:Http Request
    Return:Render Daily Report Register
    """
    if request.method == 'POST':
        form = DailyReportForm(request.POST)
        date_form = DateRangeSelectionForm(request.POST)
        if form.is_valid() and date_form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            mode_of_payment = request.POST['mode_of_payment']
            mode_name = ModeOfPayment.objects.values('method').get(id=mode_of_payment)
            list_of_report = []
            if mode_of_payment == '1':
                purchase_order = PurchaseOrder.objects.filter(date_time__range=\
                    (start_date,end_date)).filter(mode_of_payment__method=\
                    'Cash').values('date_time',\
                    'bill__amount_received',\
                    'voucherid__purchase_order_of_session',\
                    'buyer__first_name',\
                    'buyer__last_name',\
                    'buyer__customer__address__pin',\
                    'buyer__customer__user__customer__address__street_address',\
                    'buyer__customer__user__customer__address__district',\
                    'buyer__customer__title').distinct().order_by('date_time',
                    'voucherid__receipt_no_of_session')
            else:
                purchase_order = PurchaseOrder.objects.filter(date_time__range=\
                     (start_date,end_date)).exclude(mode_of_payment__method=\
                     'Cash').values('date_time',\
                     'bill__amount_received',\
                     'voucherid__purchase_order_of_session',\
                     'buyer__first_name',\
                     'buyer__last_name',\
                     'buyer__customer__address__pin',\
                     'buyer__customer__user__customer__address__street_address',\
                     'buyer__customer__user__customer__address__district',\
                     'buyer__customer__title').distinct().order_by('date_time',
                    'voucherid__receipt_no_of_session')
            temp_list = []
            result = []
            for temp_value in purchase_order:
                temp_list.append(\
                    temp_value['voucherid__purchase_order_of_session'])
                temp_list.append(temp_value['date_time'])
                if temp_value['buyer__first_name']:
                    name = temp_value['buyer__first_name']\
                    +" "+ temp_value['buyer__last_name']
                else:
                    name =temp_value['buyer__customer__title']
                temp_list.append(name)

                temp_list.append(\
                    temp_value['buyer__customer__user__customer__address__street_address'])
                temp_list.append(\
                    temp_value['buyer__customer__user__customer__address__district'])
                temp_list.append(temp_value['bill__amount_received'])
                result.append(temp_list)
                temp_list = []

            sum = 0
            for temp_var in purchase_order:
                sum = sum + temp_var['bill__amount_received']
            request_status = request_notify()
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%B-%d-%Y')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%B-%d-%Y')
            back_link=reverse('librehatti.reports.register.daily_report_result')
            return render(request,'reports/daily_report_result.html',\
            {'result':result,'sum':sum, 'mode_name':mode_name,\
            'start_date':start_date,'end_date':end_date,\
            'request':request_status, 'back_link':back_link})
        else:
            form = DailyReportForm(request.POST)
            date_form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/daily_report_form.html', \
            {'form':form,'date_form':date_form,'request':request_status})
    else:
        form = DailyReportForm()
        date_form = DateRangeSelectionForm()
        request_status = request_notify()
        return render(request,'reports/daily_report_form.html', \
        {'form':form,'date_form':date_form,'request':request_status})



@login_required
def consultancy_funds_report(request):
    """
    It generates the report which lists all
    the Consultancy Funds for the Material
    selected and the in the entered Time Span.
    Argument:Http Request
    Return:Render Consultancy Funds Register
    """
    if request.method == 'POST':
        form = ConsultancyFunds(request.POST)
        date_form = DateRangeSelectionForm(request.POST)
        if form.is_valid() and date_form.is_valid():
            category = form.cleaned_data['sub_category']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            voucher_object = VoucherId.objects.\
            filter(purchase_order__date_time__range = (start_date,end_date)).\
            filter(purchased_item__item__category__in = category, is_special=0).\
            values('purchase_order_of_session','voucher_no',\
                'session_id',\
            'purchase_order__date_time',\
            'purchase_order__buyer__first_name',\
            'purchase_order__buyer__last_name',\
            'purchase_order__buyer__customer__address__pin',\
            'purchase_order__buyer__customer__address__street_address',\
            'purchase_order__buyer__customer__address__district',\
            'purchase_order__buyer__customer__address__province',\
            'purchase_order__buyer__customer__title',\
            'purchased_item__item__category',
            'purchased_item__item__category__name').distinct()
            temp_list = []
            result = []
            consultanttotal = 0
            for temp_value in voucher_object:
                temp_list.append(temp_value['purchase_order_of_session'])
                temp_list.append(temp_value['purchase_order__date_time'])
                if temp_value['purchase_order__buyer__first_name']:
                    name = temp_value['purchase_order__buyer__first_name']\
                    +" "+ temp_value['purchase_order__buyer__last_name']
                else:
                    name =temp_value['purchase_order__buyer__customer__title']
                temp_list.append(name)
                temp_list.append(\
                    temp_value['purchase_order__buyer__customer__address__street_address'])
                temp_list.append(\
                    temp_value['purchase_order__buyer__customer__address__district'])
                consultancy_var = CalculateDistribution.objects.\
                values('consultancy_asset').get(voucher_no=
                    temp_value['voucher_no'],session_id=temp_value['session_id'])
                temp_list.append(consultancy_var['consultancy_asset'])
                temp_list.append(temp_value['purchased_item__item__category__name'])
                consultanttotal = consultanttotal +\
                consultancy_var['consultancy_asset']
                result.append(temp_list)
                temp_list = []
            category_name = Category.objects.filter(id__in=category).values('name')
            request_status = request_notify()
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%B-%d-%Y')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%B-%d-%Y')
            back_link=reverse('librehatti.reports.register.consultancy_funds_report')
            return render(request, 'reports/consultancy_funds_result.html',\
             {'result':result, 'back_link':back_link,\
                'start_date':start_date, 'end_date':end_date,\
                'sum':sum, 'category_name':category_name,\
                'request':request_status, 'consultanttotal':consultanttotal})
        else:
            form = ConsultancyFunds(request.POST)
            date_form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/consultancy_funds_form.html', \
            {'form':form,'date_form':date_form,'request':request_status})
    else:
        form = ConsultancyFunds()
        request_status = request_notify()
        date_form = DateRangeSelectionForm()
        return render(request,'reports/consultancy_funds_form.html', \
        {'form':form,'date_form':date_form,'request':request_status})

@login_required
def tds_report_result(request):
    """
    This view is used to display the TDS report registers
    Argument:Http Request
    Return:Render TDS Report Register
    """
    if request.method == 'POST':
        form = DateRangeSelectionForm(request.POST)
        if form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            purchase_order = PurchaseOrder.objects.filter(date_time__range=\
                (start_date,end_date)).values('date_time','id')
            list_of_bill = []
            billamount = 0
            tds =0
            amountreceived = 0
            grandtotal = 0
            temp_list = []
            result = []
            surcharge_values = []
            surcharge_value = Surcharge.objects.values('value').filter(\
                taxes_included=1)
            for sur_value in surcharge_value:
                surcharge_values.append(sur_value['value'])
            taxesapplied_obj = TaxesApplied.objects.values('purchase_order__id').\
            filter(purchase_order__date_time__range=(start_date,end_date),
                purchase_order__tds__gt=0)
            bill_object = Bill.objects.\
            filter(purchase_order__in=taxesapplied_obj).\
            values('purchase_order__date_time',\
            'purchase_order__id',\
            'purchase_order__buyer__first_name',\
            'purchase_order__buyer__last_name',\
            'purchase_order__buyer__customer__title',\
            'purchase_order__buyer__customer__telephone',\
            'purchase_order__buyer__customer__address__street_address',\
            'purchase_order__buyer__customer__address__district',
            'purchase_order__buyer__customer__address__pin',
            'totalplusdelivery','purchase_order__tds','amount_received'\
            ,'grand_total'\
            ,'purchase_order__buyer__customer__user__email',\
            'purchase_order__buyer__customer__telephone')
            servicetax = 0
            Heducationcess = 0
            educationcess = 0
            service_tax = 0
            education_tax = 0
            heducation_tax = 0

            list_of_taxes = []
            for temp_value in bill_object:
                flag = 1
                voucher_object = VoucherId.objects.\
                filter(purchase_order_id = temp_value['purchase_order__id']).\
                values('purchase_order_of_session').distinct()
                for value in voucher_object:
                    temp_list.append(value['purchase_order_of_session'])
                temp_list.append(temp_value['purchase_order__date_time'])
                if temp_value['purchase_order__buyer__first_name']:
                        name = temp_value['purchase_order__buyer__first_name']\
                        +" "+ temp_value['purchase_order__buyer__last_name']
                else:
                    name =temp_value['purchase_order__buyer__customer__title']
                temp_list.append(name)
                temp_list.append(temp_value[\
                'purchase_order__buyer__customer__address__street_address'])
                temp_list.append(temp_value[\
                'purchase_order__buyer__customer__address__district'])
                temp_list.append(\
                    temp_value['purchase_order__buyer__customer__telephone'])
                temp_list.append(temp_value['totalplusdelivery'])
                taxesapplied = TaxesApplied.objects.values('tax').filter(\
                purchase_order=temp_value['purchase_order__id'])
                tax_var = 0
                for taxvalue in taxesapplied:
                    temp_list.append(taxvalue['tax'])
                temp_list.append(temp_value['amount_received'])
                temp_list.append(temp_value['purchase_order__tds'])
                temp_list.append(temp_value['grand_total'])
                result.append(temp_list)
                temp_list = []

                billamount = billamount + temp_value['totalplusdelivery']
                tds = tds + temp_value['purchase_order__tds']
                amountreceived = amountreceived + temp_value['amount_received']
                grandtotal = grandtotal + temp_value['grand_total']
            tax = TaxesApplied.objects.\
            filter(purchase_order__date_time__range=(start_date,end_date),
                purchase_order__tds__gt=0).\
            values('surcharge','tax')
            for value in tax:
                list_of_taxes.append(value)

            for taxes_object_var in tax:
                if taxes_object_var['surcharge'] == 1:
                    servicetax = servicetax + taxes_object_var['tax']
                elif taxes_object_var['surcharge'] == 3:
                    Heducationcess = Heducationcess + taxes_object_var['tax']
                else:
                    educationcess = educationcess + taxes_object_var['tax']

            request_status = request_notify()
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%B-%d-%Y')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%B-%d-%Y')
            back_link=reverse('librehatti.reports.register.tds_report_result')
            return render(request,'reports/tds_report_result.html',\
            {'result':result,'request':request_status,\
            'servicetax':servicetax,'Heducationcess':Heducationcess,\
            'educationcess':educationcess,'start_date':start_date,\
            'grandtotal':grandtotal,'end_date':end_date,\
            'billamount':billamount,'tds':tds,'amountreceived':amountreceived,\
            'surcharge_values':surcharge_values, 'back_link':back_link})

        else:
            form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/tds_report_form.html', \
            {'form':form,'request':request_status})
    else:
        form = DateRangeSelectionForm()
        request_status = request_notify()
        return render(request,'reports/tds_report_form.html', \
        {'form':form,'request':request_status})

@login_required
def payment_register(request):
    """
    This view is used to display the payment registers
    Argument:Http Request
    Return:Render Payment Register
    """
    if request.method == 'POST':
        form = DateRangeSelectionForm(request.POST)
        if form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            service_tax = 0
            education_tax = 0
            heducation_tax = 0
            billamount = 0
            tds =0
            amountreceived = 0
            temp_list = []
            result = []
            surcharge_values = []
            surcharge_value = Surcharge.objects.values('value').filter(\
                taxes_included=1)
            for sur_value in surcharge_value:
                surcharge_values.append(sur_value['value'])
            taxesapplied_obj = TaxesApplied.objects.values('purchase_order__id').\
            filter(purchase_order__date_time__range=(start_date,end_date))
            bill_object = Bill.objects.filter(
                purchase_order__in=taxesapplied_obj).\
            values('purchase_order__date_time',\
            'purchase_order__id',\
            'purchase_order__buyer__first_name',\
            'purchase_order__buyer__last_name',\
            'purchase_order__buyer__customer__title',\
            'purchase_order__buyer__customer__address__street_address',\
            'purchase_order__buyer__customer__address__district',
            'purchase_order__buyer__customer__address__pin',
            'totalplusdelivery','purchase_order__tds','amount_received'\
            ,'purchase_order__buyer__customer__user__email',\
            'purchase_order__buyer__customer__telephone',\
            'purchase_order__buyer__customer__company',
            'purchase_order__delivery_address').order_by('id')
            servicetax = 0
            Heducationcess = 0
            educationcess = 0
            list_of_taxes = []
            for temp_value in bill_object:
                flag = 1
                voucher_object = VoucherId.objects.\
                filter(purchase_order_id = temp_value['purchase_order__id']).\
                values('purchase_order_of_session','voucher_no').distinct()
                for value in voucher_object:
                    purchase_order_of_session=value['purchase_order_of_session']
                temp_list.append(purchase_order_of_session)
                temp_list.append(temp_value['purchase_order__date_time'])
                if temp_value['purchase_order__buyer__first_name']:
                    name = temp_value['purchase_order__buyer__first_name']\
                    +" "+ temp_value['purchase_order__buyer__last_name']
                else:
                    name =\
                    temp_value['purchase_order__buyer__customer__title']
                temp_list.append(name)
                temp_list.append(temp_value[\
                'purchase_order__buyer__customer__address__street_address'])
                temp_list.append(temp_value[\
                'purchase_order__buyer__customer__address__district'])
                temp_list.append(temp_value[\
                'purchase_order__buyer__customer__company'])


                material = PurchasedItem.objects.values\
                ('item__category__name').\
                filter(purchase_order__id =\
                    temp_value['purchase_order__id']).distinct()
                for item in material:
                    if flag == 1:
                        material_list = item['item__category__name']
                        flag = 0
                    else:
                       material_list = material_list + ', ' +\
                       item['item__category__name']
                temp_list.append(material_list)
                temp_list.append(temp_value['purchase_order__delivery_address'])
                temp_list.append(temp_value[\
                'purchase_order__buyer__customer__telephone'])
                temp_list.append(temp_value[\
                'purchase_order__buyer__customer__user__email'])
                temp_list.append(temp_value['totalplusdelivery'])
                taxesapplied = TaxesApplied.objects.values('tax').filter(\
                purchase_order=temp_value['purchase_order__id'])
                for taxvalue in taxesapplied:
                    temp_list.append(taxvalue['tax'])
                temp_list.append(temp_value['purchase_order__tds'])
                temp_list.append(temp_value['amount_received'])
                result.append(temp_list)
                print (temp_list[0],",",temp_list[1],",",temp_list[2],",",temp_list[6],",",temp_list[7],",",temp_list[10]+temp_list[11]+temp_list[12]+temp_list[13])
                temp_list = []
                material_list = ''
                billamount = billamount + temp_value['totalplusdelivery']
                tds = tds + temp_value['purchase_order__tds']
                amountreceived = amountreceived + temp_value['amount_received']

            tax = TaxesApplied.objects.\
            filter(purchase_order__date_time__range=(start_date,end_date)).\
            values('surcharge','tax')
            for value in tax:
                list_of_taxes.append(value)

            for taxes_object_var in tax:
                if taxes_object_var['surcharge'] == 1:
                    servicetax = servicetax + taxes_object_var['tax']
                elif taxes_object_var['surcharge'] == 3:
                    Heducationcess = Heducationcess + taxes_object_var['tax']
                else:
                    educationcess = educationcess + taxes_object_var['tax']

            request_status = request_notify()
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%B-%d-%Y')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%B-%d-%Y')
            back_link=reverse('librehatti.reports.register.payment_register')
            return render(request,'reports/payment_register_result.html',\
            {'result':result,'request':request_status,\
            'servicetax':servicetax,'Heducationcess':Heducationcess,\
            'educationcess':educationcess,'start_date':start_date,\
            'end_date':end_date,'billamount':billamount,\
            'tds':tds,'amountreceived':amountreceived,\
            'surcharge_values':surcharge_values, 'back_link':back_link})
        else:
            form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/payment_register_form.html', \
            {'form':form,'request':request_status})
    else:
        form = DateRangeSelectionForm()
        request_status = request_notify()
        return render(request,'reports/payment_register_form.html', \
        {'form':form,'request':request_status})


@login_required
def suspense_clearance_register(request):
    """
    This view is used to display the suspense clearance registers
    Argument:Http Request
    Return:Render Suspense Clearance Register
    """
    if request.method == 'POST':
        form = DateRangeSelectionForm(request.POST)
        if form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            suspenseclearance = SuspenseClearance.objects.values('voucher_no',
            'session_id').filter(clear_date__range=(start_date,end_date))
            distribution = Distribution.objects.values('college_income',\
                'admin_charges').filter()[0]
            result = []
            temp = []
            for value in suspenseclearance:
                suspense = SuspenseOrder.objects.filter(is_cleared=1,
                voucher=value['voucher_no'],
                session_id=value['session_id'])
                if not suspense:
                    continue
                suspense = SuspenseOrder.objects.values('voucher',\
                    'session_id', 'purchase_order', 'purchase_order__date_time',\
                    'purchase_order__buyer__first_name',\
                    'purchase_order__buyer__last_name',\
                    'purchase_order__buyer__customer__title',\
                    'purchase_order__buyer__customer__address__street_address',\
                    'purchase_order__buyer__customer__address__district',\
                    'purchase_order__buyer__customer__address__pin',\
                    'purchase_order__buyer__customer__address__province').\
                filter(is_cleared=1, voucher=value['voucher_no'],
                session_id=value['session_id'])[0]
                temp.append(suspense['voucher'])
                cleared_voucher_no = SuspenseClearedRegister.objects.values(
                    'suspenseclearednumber').filter(voucher_no=suspense['voucher'],
                    session_id=suspense['session_id'])[0]
                temp.append(cleared_voucher_no['suspenseclearednumber'])
                temp.append(suspense['purchase_order__date_time'])
                voucherid = VoucherId.objects.values(\
                    'purchase_order_of_session').filter(\
                    voucher_no=suspense['voucher'],\
                    session_id=suspense['session_id'])[0]
                temp.append(voucherid['purchase_order_of_session'])
                if suspense['purchase_order__buyer__first_name']:
                    if suspense[\
                    'purchase_order__buyer__customer__address__pin'] == None:
                        address = suspense['purchase_order__buyer__first_name']\
                        + suspense['purchase_order__buyer__last_name']\
                        + ', ' +\
                        suspense[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__province']
                    else:
                        address = suspense['purchase_order__buyer__first_name'] +\
                        suspense['purchase_order__buyer__last_name'] +\
                        ', ' +\
                        suspense[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__province']
                else:
                    if suspense[\
                    'purchase_order__buyer__customer__address__pin'] == None:
                        address =\
                        suspense['purchase_order__buyer__customer__title']\
                        + ', ' +\
                        suspense[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__province']
                    else:
                        address =\
                        suspense['purchase_order__buyer__customer__title'] +\
                        ', ' +\
                        suspense[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__province']
                temp.append(address)
                voucherid = VoucherId.objects.values(\
                    'purchase_order__purchaseditem__item__category__name').\
                filter(voucher_no=suspense['voucher'],\
                    session_id=suspense['session_id'])[0]
                temp.append(voucherid[\
                    'purchase_order__purchaseditem__item__category__name'])
                caldistribute = CalculateDistribution.objects.values(\
                    'college_income_calculated', 'admin_charges_calculated',\
                    'consultancy_asset', 'development_fund', 'total').get(voucher_no=\
                    suspense['voucher'], session_id=suspense['session_id'])
                temp.append(caldistribute['college_income_calculated'])
                temp.append(caldistribute['admin_charges_calculated'])
                temp.append(caldistribute['consultancy_asset'])
                temp.append(caldistribute['development_fund'])
                try:
                    transport = Transport.objects.values('total').get(voucher_no=\
                        suspense['voucher'], session_id=suspense['session_id'])
                    trans_value = transport['total']
                    temp.append(trans_value)
                except:
                    trans_value = 0
                    temp.append(trans_value)
                try:
                    tada = TaDa.objects.values('tada_amount').get(voucher_no=\
                        suspense['voucher'], session=suspense['session_id'])
                    tada_value = tada['tada_amount']
                    temp.append(tada_value)
                except:
                    tada_value = 0
                    temp.append(tada_value)
                try:
                    suspensecl = SuspenseClearance.objects.values(\
                        'work_charge', 'labour_charge', 'car_taxi_charge',\
                        'boring_charge_external', 'boring_charge_internal').get(\
                        voucher_no=suspense['voucher'],\
                        session_id=suspense['session_id'],\
                        clear_date__range=(start_date,end_date))
                    other_charges = suspensecl['labour_charge'] +\
                    suspensecl['car_taxi_charge'] +\
                    suspensecl['boring_charge_external']
                    temp.append(suspensecl['work_charge'])
                    temp.append(other_charges)
                    temp.append(suspensecl['boring_charge_internal'])
                    grand_total = caldistribute['total'] + trans_value + tada_value\
                    + suspensecl['work_charge'] + other_charges +\
                    suspensecl['boring_charge_internal']
                    temp.append(grand_total)
                    result.append(temp)
                except:
                    pass
                temp = []
                address = ''
            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.suspense_clearance_register')
            return render(request,'reports/suspense_clearance_result.html',\
            {'result':result, 'request':request_status,\
            'distribution':distribution, 'back_link':back_link})
        else:
            form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/suspense_clearance_form.html', \
            {'form':form,'request':request_status})
    else:
        form = DateRangeSelectionForm()
        request_status = request_notify()
        return render(request,'reports/suspense_clearance_form.html', \
        {'form':form,'request':request_status})

Teacher=["Prof. kulbir Sing Gill","Dr. B.S. Walia","Dr. B.S. Walia","Prof. Harjinder Singh", "Prof. Gurdeepak Singh", "Dr. Harpal Singh", "Dr. Hardeep Singh"," Dr. Harvinder Singh","Prof. Parshant Garg", "Prof. K.S. Bedi","Prof. K.S. Bedi","Prof. K.S. Bedi","Prof. K.S. Bedi","Prof. K.S. Bedi","Dr. Jagbir Singh","Dr. Jagbir Singh","Dr. Jagbir Singh","Dr. Jagbir Singh","Dr.R.P.Singh", "Prof. Puneet Pal Singh"]


def servicetax_registerYear(year):
    """
    This view is used to display the servicetax_register registers
    Argument:Http Request
    Return:Render Service Tax Register
    """
    #p = inflect.engine()
    total = 0
    totalplustax = 0
    taxes_name = TaxesApplied.objects.values('surcharge_name','surcharge_value').\
    filter(
        purchase_order__date_time__year=year).distinct()
    paid_taxes = {}
    init_taxes = {}
    not_paid_taxes = {}
    surcharges = Surcharge.objects.filter()
    for val in surcharges:
        for val2 in taxes_name:
            if val.tax_name in val2['surcharge_name']:
                init_taxes['%s' % val.tax_name.replace(" ", "_").lower()] = 0
    taxesapplied_obj = TaxesApplied.objects.values('purchase_order__id').\
    filter(
        purchase_order__date_time__year=year).order_by('purchase_order__date_time')
    purchase_order = PurchaseOrder.objects.values('date_time', 'id',\
        'bill__totalplusdelivery', 'bill__grand_total',\
        'buyer__first_name', 'buyer__last_name',\
	'buyer__customer__gst_in',\
        'buyer__customer__title',\
        'buyer__customer__address__street_address',\
        'buyer__customer__address__district',\
        'buyer__customer__address__pin',\
        'buyer__customer__address__province',).\
    filter(id__in=taxesapplied_obj).order_by('date_time')
    result = []
    for value in purchase_order:
        i=0
        temp = []
        voucherid = VoucherId.objects.values(\
            'purchase_order_of_session').filter(\
            purchase_order=value['id'])
        if(len(voucherid)==0):
            temp.append("Nil")
        else:   
            temp.append(voucherid[0]['purchase_order_of_session'])
        temp.append(value['date_time'])
        if value['buyer__first_name']:
            address = value['buyer__first_name']\
            + value['buyer__last_name']\
            + ', ' +\
            value[\
            'buyer__customer__address__street_address']\
            + ', ' + \
            value[\
            'buyer__customer__address__district']\
            + ', ' + \
            value[\
            'buyer__customer__address__province']
        else:
            address =\
            value['buyer__customer__title']\
            + ', ' +\
            value[\
            'buyer__customer__address__street_address']\
            + ', ' + \
            value[\
            'buyer__customer__address__district']\
            + ', ' + \
            value[\
            'buyer__customer__address__province']
        if value['buyer__customer__gst_in']:
            gst_in = value['buyer__customer__gst_in']
        else:
            gst_in = ''
        temp.append(address)
        temp.append(gst_in)
        temp.append(value['bill__totalplusdelivery'])
        total = total+value['bill__totalplusdelivery']
        tax_data = []
        for val in taxes_name:
            taxesapplied = TaxesApplied.objects.values('tax', 'surcharge_name').filter(\
                purchase_order=value['id'], surcharge_name=val['surcharge_name'])
            if taxesapplied:
                taxesapplied = TaxesApplied.objects.values('tax', 'surcharge_name').filter(\
                    purchase_order=value['id'], surcharge_name=val['surcharge_name'])[0]
                init_taxes[val['surcharge_name'].replace(" ", "_").lower()]\
                = init_taxes[val['surcharge_name'].replace(" ", "_").lower()] + taxesapplied['tax']
                tax_data.append(taxesapplied['tax'])
            else:
                tax_data.append('0')
        temp.append(tax_data)
        temp.append(value['bill__grand_total'])
        totalplustax = totalplustax +\
        value['bill__grand_total']
        materiallist=""
        material = VoucherId.objects.\
        values(\
            'purchased_item__item_id__category__name').filter(\
            purchase_order=value['id']).distinct()
        for i in material:
            if(materiallist== ""):
                materiallist=i['purchased_item__item_id__category__name']

            else:
                materiallist=materiallist+" , "+i['purchased_item__item_id__category__name']
        print (temp[0],"|",temp[1],"|",Teacher[randint(0,19)],"|",temp[2],"|",materiallist,"|",temp[5])#,"|",p.number_to_word(temp[5])

@login_required
def servicetax_register(request):
    """
    This view is used to display the servicetax_register registers
    Argument:Http Request
    Return:Render Service Tax Register
    """
    if request.method == 'POST':
        form = MonthYearForm(request.POST)
        data_form = PaidTaxesForm(request.POST)
        if form.is_valid() and data_form.is_valid():
            month = request.POST['month']
            year = request.POST['year']
            servicetax_registerYear(year)
            total = 0
            totalplustax = 0
            taxes_name = TaxesApplied.objects.values('surcharge_name','surcharge_value').\
            filter(purchase_order__date_time__month=month,
                purchase_order__date_time__year=year).distinct()
            paid_taxes = {}
            init_taxes = {}
            not_paid_taxes = {}
            surcharges = Surcharge.objects.filter()
            for val in surcharges:
                for val2 in taxes_name:
                    if val.tax_name in val2['surcharge_name']:
                        paid_taxes['%s' % val.tax_name.replace(" ", "_").lower()]\
                        = data_form.cleaned_data['paid_' + val.tax_name.replace(" ", "_").lower()]
                        init_taxes['%s' % val.tax_name.replace(" ", "_").lower()] = 0
            taxesapplied_obj = TaxesApplied.objects.values('purchase_order__id').\
            filter(purchase_order__date_time__month=month,
                purchase_order__date_time__year=year).order_by('purchase_order__date_time')
            purchase_order = PurchaseOrder.objects.values('date_time', 'id',\
                'bill__totalplusdelivery', 'bill__grand_total',\
                'buyer__first_name', 'buyer__last_name',\
                'buyer__customer__title',\
                'buyer__customer__address__street_address', 'buyer__customer__gst_in',\
	        'buyer__customer__telephone',\
                'buyer__customer__address__district',\
                'buyer__customer__address__pin',\
                'buyer__customer__address__province').\
            filter(id__in=taxesapplied_obj).order_by('date_time')
            result = []
            for value in purchase_order:
                i=0
                temp = []
                voucherid = VoucherId.objects.values(\
                    'purchase_order_of_session').filter(\
                    purchase_order=value['id'])[0]
                temp.append(voucherid['purchase_order_of_session'])
                temp.append(value['date_time'])
                if value['buyer__first_name']:
                    address = value['buyer__first_name']\
                    + value['buyer__last_name']\
                    + ', ' +\
                    value[\
                    'buyer__customer__address__street_address']\
                    + ', ' + \
                    value[\
                    'buyer__customer__address__district']\
                    + ', ' + \
                    value[\
                    'buyer__customer__address__province']
                else:
                    address =\
                    value['buyer__customer__title']\
                    + ', ' +\
                    value[\
                    'buyer__customer__address__street_address']\
                    + ', ' + \
                    value[\
                    'buyer__customer__address__district']\
                    + ', ' + \
                    value[\
                    'buyer__customer__address__province']
               	if value['buyer__customer__gst_in']:
                    gst_in = value['buyer__customer__gst_in']
                else:
                    gst_in = ''
                telephone = value['buyer__customer__telephone']
                temp.append(address)
                temp.append(gst_in)
                temp.append(value['bill__totalplusdelivery'])
                total = total+value['bill__totalplusdelivery']
                tax_data = []
                for val in taxes_name:
                    taxesapplied = TaxesApplied.objects.values('tax', 'surcharge_name').filter(\
                        purchase_order=value['id'], surcharge_name=val['surcharge_name'])
                    if taxesapplied:
                        taxesapplied = TaxesApplied.objects.values('tax', 'surcharge_name').filter(\
                            purchase_order=value['id'], surcharge_name=val['surcharge_name'])[0]
                        init_taxes[val['surcharge_name'].replace(" ", "_").lower()]\
                        = init_taxes[val['surcharge_name'].replace(" ", "_").lower()] + taxesapplied['tax']
                        tax_data.append(taxesapplied['tax'])
                    else:
                        tax_data.append('0')
                temp.append(tax_data)
                temp.append(value['bill__grand_total'])
                temp.append(telephone)
                totalplustax = totalplustax +\
                value['bill__grand_total']
                result.append(temp)
                address = ''
            total_taxes = sum(init_taxes.values())
            for val in surcharges:
                for val2 in taxes_name:
                    if val.tax_name in val2['surcharge_name']:
                        not_paid_taxes['%s' % val.tax_name.replace(" ", "_").lower()]\
                        = init_taxes['%s' % val.tax_name.replace(" ", "_").lower()] - paid_taxes['%s' % val.tax_name.replace(" ", "_").lower()]
            total_taxes_not_paid = sum(not_paid_taxes.values())
            request_status = request_notify()
            month = calendar.month_name[int(month)]
            back_link=reverse('librehatti.reports.register.servicetax_register')
            return render(request,'reports/servicetax_statement.html',\
            {'result':result, 'request':request_status, 'month':month,\
            'year':year, 'total':total, 'taxes_name':taxes_name,\
            'totalplustax':totalplustax, 'init_taxes':init_taxes,
            'not_paid_taxes':not_paid_taxes,
            'paid_taxes':paid_taxes, 'total_taxes':total_taxes,
            'total_taxes_not_paid':total_taxes_not_paid})
        else:
            form = MonthYearForm(request.POST)
            data_form = PaidTaxesForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/servicetax_form.html', \
            {'form':form, 'data_form':data_form, 'request':request_status})
    else:
        form = MonthYearForm()
        data_form = PaidTaxesForm()
        request_status = request_notify()
        return render(request,'reports/servicetax_form.html', \
        {'form':form, 'data_form':data_form, 'request':request_status})


@login_required
def main_register(request):
    """
    This view is used to display the Main register
    Argument:Http Request
    Return:Render Main Register
    """
    if request.method == 'POST':
        form = MonthYearForm(request.POST)
        if form.is_valid():
            month = request.POST['month']
            year = request.POST['year']
            list_of_client = []
            suspense_order = SuspenseOrder.objects.\
            values_list('purchase_order', flat=True).\
            filter(purchase_order__date_time__month=month).\
            filter(purchase_order__date_time__year=year)
            purchase_order = PurchaseOrder.objects.\
            filter(date_time__month = month).\
            filter(date_time__year = year).\
            values('voucherid__purchase_order_of_session',\
                'voucherid__session',\
                'voucherid__voucher_no',\
                'date_time',\
                'buyer__first_name',\
                'buyer__last_name',\
                'buyer__customer__address__pin',\
                'buyer__customer__title',\
                'buyer__customer__address__street_address',\
                'buyer__customer__address__district',\
                'buyer__customer__address__province',\
                ).exclude(id__in = suspense_order).\
            exclude(voucherid__is_special=1).distinct().order_by('date_time',\
                'voucherid__receipt_no_of_session')
            distribution = Distribution.objects.values('college_income',\
                'admin_charges').filter()[0]
            temp_list = []
            result = []
            collegeincometotal = 0
            adminchargestotal = 0
            consultanttotal = 0
            developmenttotal = 0
            distributiontotal = 0
            for temp_value in purchase_order:
                temp_list.append(temp_value['voucherid__purchase_order_of_session'])
                temp_list.append(temp_value['date_time'])
                if temp_value['buyer__first_name']:
                        name = temp_value['buyer__first_name']\
                        + temp_value['buyer__last_name']
                else:
                        name =temp_value['buyer__customer__title']
                temp_list.append(name)
                temp_list.append(
                        temp_value[\
                        'buyer__customer__address__street_address']\
                        + ', ' + \
                        temp_value[\
                        'buyer__customer__address__district']\
                        + ', ' + \
                        temp_value[\
                        'buyer__customer__address__province'])
                material = VoucherId.objects.\
                values('purchased_item__item_id__category__name').\
                filter(voucher_no = temp_value['voucherid__voucher_no'],
                    session_id = temp_value['voucherid__session']).distinct()
                for value in material:
                    temp_list.append(\
                        value['purchased_item__item_id__category__name'])
                calculated_distribution = CalculateDistribution.objects.\
                    filter(voucher_no=temp_value['voucherid__voucher_no'])\
                    .filter(session = temp_value['voucherid__session'])\
                    .values('college_income_calculated',\
                    'admin_charges_calculated',\
                    'consultancy_asset','development_fund','total')[0]
                temp_list.append(calculated_distribution['college_income_calculated'])
                temp_list.append(calculated_distribution['admin_charges_calculated'])
                temp_list.append(calculated_distribution['consultancy_asset'])
                temp_list.append(calculated_distribution['development_fund'])
                temp_list.append(calculated_distribution['total'])
                collegeincometotal = collegeincometotal +\
                calculated_distribution['college_income_calculated']
                adminchargestotal = adminchargestotal +\
                calculated_distribution['admin_charges_calculated']
                consultanttotal = consultanttotal +\
                calculated_distribution['consultancy_asset']
                developmenttotal = developmenttotal +\
                calculated_distribution['development_fund']
                distributiontotal = distributiontotal +\
                calculated_distribution['total']
                result.append(temp_list)
                temp_list = []
            month_name = calendar.month_name[int(month)]
            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.main_register')
            return render(request,'reports/main_register_result.html',\
            {'request':request_status, 'distribution':distribution,\
             'result':result,'month':month_name,'year':year,
             'back_link':back_link, 'collegeincometotal':collegeincometotal,
             'adminchargestotal':adminchargestotal,
             'consultanttotal':consultanttotal,
             'developmenttotal':developmenttotal,
             'distributiontotal':distributiontotal})
        else:
            form = MonthYearForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/main_register_form.html', \
            {'form':form,'request':request_status})
    else:
        form = MonthYearForm()
        request_status = request_notify()
        return render(request,'reports/main_register_form.html', \
        {'form':form,'request':request_status})


@login_required
def proforma_register(request):
    """
    This view is used to display the proforma registers
    Argument:Http Request
    Return:Render Proforma Register
    """
    if request.method == 'POST':
        form = DateRangeSelectionForm(request.POST)
        if form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            quotedtaxesapplied = QuotedTaxesApplied.objects.\
            values('quoted_order__id').filter(
                quoted_order__date_time__range=(start_date,end_date))
            quotedorder = QuotedOrder.objects.values('id',\
                'quotedorderofsession__quoted_order_session', 'date_time',\
                'buyer__first_name', 'buyer__last_name',\
                'buyer__customer__title',\
                'buyer__customer__address__street_address',\
                'buyer__customer__address__district',\
                'buyer__customer__company',\
                'buyer__email', 'quotedbill__totalplusdelivery',\
                'quotedbill__grand_total', 'delivery_address').filter(\
                id__in=quotedtaxesapplied)
            temp = []
            result = []
            material_list = ''
            flag = 1
            surcharge_values = []
            surcharge_value = Surcharge.objects.values('value').filter(\
                taxes_included=1)
            for sur_value in surcharge_value:
                surcharge_values.append(sur_value['value'])
            for order in quotedorder:
                temp.append(order[\
                    'quotedorderofsession__quoted_order_session'])
                temp.append(order['date_time'])
                if order['buyer__first_name']:
                    name = order['buyer__first_name'] + ' ' +\
                    order['buyer__last_name']
                else:
                    name = order['buyer__customer__title']
                temp.append(name)
                temp.append(order['buyer__customer__address__street_address'])
                temp.append(order['buyer__customer__address__district'])
                temp.append(order['buyer__customer__company'])
                quoteditem = QuotedItem.objects.values('item__category__name',\
                    'item__category__id').\
                filter(quoted_order=order['id']).distinct()
                for item in quoteditem:
                    if flag == 1:
                        material_list = item['item__category__name']
                        flag = 0
                    else:
                        material_list = material_list + ', ' +\
                        item['item__category__name']
                temp.append(material_list)
                temp.append(order['delivery_address'])
                #temp.append(order['buyer__customer__telephone'])
                temp.append(order['buyer__email'])
                temp.append(order['quotedbill__totalplusdelivery'])
                taxes = QuotedTaxesApplied.objects.values('tax').filter(\
                    quoted_order=order['id'])
                for taxvalue in taxes:
                    temp.append(taxvalue['tax'])
                temp.append(order['quotedbill__grand_total'])
                result.append(temp)
                temp = []
                flag = 1
                material_list = ''
                name = ''
            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.proforma_register')
            return render(request,'reports/proforma_register.html',\
            {'result':result, 'request':request_status,\
            'surcharge_values':surcharge_values, 'back_link':back_link})
        else:
            form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/proforma_reg_form.html', \
            {'form':form,'request':request_status})
    else:
        form = DateRangeSelectionForm()
        request_status = request_notify()
        return render(request,'reports/proforma_reg_form.html', \
        {'form':form,'request':request_status})


@login_required
def non_payment_register(request):
    """
    This view is used to display the non payment registers
    Argument:Http Request
    Return:Render Non-Payment Register
    """
    if request.method == 'POST':
        form = DateRangeSelectionForm(request.POST)
        if form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            non_payment_order = NonPaymentOrder.objects.values('id',\
                'buyer__first_name', 'buyer__last_name', 'date',\
                'buyer__customer__title', 'buyer__customer__address__pin',\
                'buyer__customer__address__street_address',\
                'buyer__customer__address__district',\
                'buyer__customer__address__province', 'reference',\
                'reference_date', 'item_type', 'delivery_address').filter(\
                date__range=(start_date,end_date))
            temp = []
            result = []
            for order in non_payment_order:
                nonpaymentorderofsession = NonPaymentOrderOfSession.objects.\
                values('non_payment_order_of_session').\
                get(non_payment_order=order['id'])
                temp.append(nonpaymentorderofsession['non_payment_order_of_session'])
                temp.append(order['date'])
                if order['buyer__first_name']:
                    name = order['buyer__first_name'] + ' ' +\
                    order['buyer__last_name']
                else:
                    name = order['buyer__customer__title']
                temp.append(name)
                if order['buyer__customer__address__pin'] == 'None':
                    address = order['buyer__customer__address__street_address']\
                    + ', ' + order['buyer__customer__address__district'] + ', ' +\
                    order['buyer__customer__address__province']
                else:
                    address = order['buyer__customer__address__street_address']\
                    + ', ' + order['buyer__customer__address__district'] + ', ' +\
                    order['buyer__customer__address__pin'] + ', ' +\
                    order['buyer__customer__address__province']
                temp.append(address)
                temp.append(order['reference'])
                temp.append(order['reference_date'])
                temp.append(order['item_type'])
                temp.append(order['delivery_address'])
                result.append(temp)
                temp = []
                address = ''
            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.non_payment_register')
            return render(request,'reports/non_payment_register.html',\
            {'result':result, 'request':request_status, 'back_link':back_link})
        else:
            form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/non_payment_form.html', \
            {'form':form,'request':request_status})
    else:
        form = DateRangeSelectionForm()
        request_status = request_notify()
        return render(request,'reports/non_payment_form.html', \
        {'form':form,'request':request_status})

@login_required
def client_register(request):
    """
    This view is used to display the client register
    Argument:Http Request
    Return:Render Client Register
    """
    if request.method == 'POST':
        form = DateRangeSelectionForm(request.POST)
        if form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            list_of_client = []
            purchase_order = PurchaseOrder.objects.filter(date_time__range=\
                (start_date,end_date)).values(
                'date_time',\
                'buyer__first_name',\
                'buyer__last_name',\
                'buyer__customer__address__pin',\
                'buyer__customer__address__street_address',\
                'buyer__customer__address__district',\
                'buyer__customer__address__province',\
                'buyer__customer__telephone',\
                'buyer__customer__user__email',\
                'buyer__customer__company',\
                'organisation__organisation_type__type_desc',\
                'buyer__customer__title')
            temp_list = []
            result = []
            for temp_value in purchase_order:
                    temp_list.append(temp_value['date_time'])
                    if temp_value['buyer__first_name']:
                        name = temp_value['buyer__first_name']\
                        + temp_value['buyer__last_name']
                    else:
                        name = temp_value['buyer__customer__title']
                    temp_list.append(name)
                    temp_list.append(\
                        temp_value['buyer__customer__address__street_address'])
                    temp_list.append(\
                        temp_value['buyer__customer__company'])
                    temp_list.append(\
                        temp_value['buyer__customer__address__district'])
                    temp_list.append(\
                        temp_value['buyer__customer__address__pin'])
                    temp_list.append(\
                        temp_value['buyer__customer__address__province'])
                    temp_list.append(\
                        temp_value['buyer__customer__user__email'])
                    temp_list.append(\
                        temp_value['buyer__customer__telephone'])
                    temp_list.append(\
                        temp_value['organisation__organisation_type__type_desc'])

                    result.append(temp_list)
                    temp_list = []
            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.client_register')
            return render(request,'reports/client_register_result.html',\
            {'request':request_status, 'result':result, 'back_link':back_link})
        else:
            form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/client_register_form.html', \
            {'form':form,'request':request_status})
    else:
        form = DateRangeSelectionForm()
        request_status = request_notify()
        return render(request,'reports/client_register_form.html', \
        {'form':form,'request':request_status})


@login_required
def material_report(request):
    """
    This view is used to display the lab reports
    Argument:Http Request
    Return:Render Lab Report
    """
    if request.method == 'POST':
        form = ConsultancyFunds(request.POST)
        date_form = DateRangeSelectionForm(request.POST)
        if form.is_valid() and date_form.is_valid():
            category = form.cleaned_data['sub_category']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            if start_date > end_date:
                error_type = "Date range error"
                error = "Start date cannot be greater than end date"
                request_status = request_notify()
                temp = {'type':error_type, 'message':error}
                return render(request, 'error_page.html', temp)

            purchase_item = PurchasedItem.objects.\
            filter(purchase_order__date_time__range=(start_date, end_date),\
                item__category__in=category).values(\
                'purchase_order_id', 'purchase_order__date_time', 'price',
                'purchase_order__buyer__first_name',
                'purchase_order__buyer__last_name',
                'purchase_order__buyer__customer__title',
                'purchase_order__buyer__customer__company',
                'purchase_order__buyer__customer__address__street_address',
                'purchase_order__buyer__customer__address__district',
                'purchase_order__buyer__customer__address__pin',
                'purchase_order__buyer__customer__address__province',
                'purchase_order__buyer__email','purchase_order__delivery_address',\
                'purchase_order__buyer__customer__telephone',
                'voucherid__purchase_order_of_session',
                'item__category__name')
            
            total_amount_sum = 0
            tax_list = Surcharge.objects.all().order_by('id')
            for value in purchase_item:
                applied_tax_list = []
                for tax in tax_list:
                    try:
                        taxes_applied = TaxesApplied.objects.filter(purchase_order=
                        value['purchase_order_id'], surcharge_id=tax.id)[0]
                        applied_tax_list.append(taxes_applied.tax)
                    except:
                        applied_tax_list.append('N.A')
                    
                value['applied_tax_list'] = applied_tax_list
                
                total_tax = TaxesApplied.objects.filter(purchase_order=
                value['purchase_order_id']).aggregate(Sum('tax'))
                value['total_amount'] = total_tax['tax__sum'] + value['price']
                total_amount_sum = value['total_amount'] + total_amount_sum
            
            category_name = Category.objects.values('name').filter(id__in=category)

            total = PurchasedItem.objects.filter(purchase_order__date_time__range
                = (start_date,end_date),item__category__in=category).\
                aggregate(Sum('price')).get('price__sum', 0.00)
            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.material_report')
            return render(request, 'reports/material_report.html', {'purchase_item':
                           purchase_item,'start_date':start_date, 'end_date':end_date,
                          'total_cost':total, 'category_name':category_name,\
                          'request':request_status, 'back_link':back_link,
                          'total_amount_sum':total_amount_sum, 'tax_list':tax_list})
        else:
            form = ConsultancyFunds(request.POST)
            date_form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/material_report_form.html', \
            {'form':form,'date_form':date_form,'request':request_status})
    else:
        form = ConsultancyFunds()
        request_status = request_notify()
        date_form = DateRangeSelectionForm()
        return render(request,'reports/material_report_form.html', \
        {'form':form,'date_form':date_form,'request':request_status})


@login_required
def suspense_register(request):
    """
    This view is used to display the suspense registers
    Argument:Http Request
    Return:Render Suspense Register
    """
    if request.method == 'POST':
        form = DateRangeSelectionForm(request.POST)
        if form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            suspenseorder = SuspenseOrder.objects.filter(
                purchase_order__date_time__range=(start_date, end_date)).values(
                'voucher', 'session_id', 'purchase_order__buyer__first_name',
                'purchase_order__buyer__last_name',
                'purchase_order__buyer__customer__title',
                'purchase_order__buyer__customer__address__street_address',
                'purchase_order__buyer__customer__address__district',
                'purchase_order__buyer__customer__address__pin',
                'purchase_order__buyer__customer__address__province',
                'purchase_order__bill__total_cost', 'purchase_order__date_time',
                'purchase_order__bill__totalplusdelivery',
                'purchase_order__bill__grand_total', 'purchase_order__tds',
                'purchase_order__bill__amount_received',
                'purchase_order__mode_of_payment__method',
                'purchase_order__cheque_dd_number', 'purchase_order',
                'purchase_order__cheque_dd_date', 'distance_estimated').\
                order_by('purchase_order__date_time','voucher')
            rate = Surcharge.objects.values('value').get(tax_name='Transportation')
            result = []
            previous_order = 0
            amount = 0
            transport_total = 0
            amountplustransport = 0
            totalbillamount = 0
            grandtotalamount = 0
            totaltds = 0
            totalamountreceived = 0
            servicetaxtotal = 0
            educationcesstotal = 0
            heducationcesstotal = 0
            for value in suspenseorder:
                flag = 1
                temp_list = []
                address = ''
                amountplustrans = 0
                temp_list.append(value['voucher'])
                voucherid = VoucherId.objects.filter(voucher_no=value['voucher'],
                    session_id=value['session_id']).values(
                    'purchase_order_of_session',
                    'purchased_item__item_id__category__name')[0]
                temp_list.append(voucherid['purchase_order_of_session'])
                temp_list.append(value['purchase_order__date_time'])
                if value['purchase_order__buyer__first_name']:
                    name = value['purchase_order__buyer__first_name'] + ' ' +\
                    value['purchase_order__buyer__last_name']
                else:
                    name = value['purchase_order__buyer__customer__title']
                temp_list.append(name)
                if value['purchase_order__buyer__customer__address__pin'] != 'None':
                    address = ', ' + \
                    value['purchase_order__buyer__customer__address__street_address'] +\
                    ', ' + value['purchase_order__buyer__customer__address__district'] +\
                    '-' + value['purchase_order__buyer__customer__address__pin'] +\
                    ', ' + value['purchase_order__buyer__customer__address__province']
                else:
                    address = ', ' + \
                    value['purchase_order__buyer__customer__address__street_address'] + \
                    ', ' + value['purchase_order__buyer__customer__address__district'] +\
                    ', ' + value['purchase_order__buyer__customer__address__province']
                temp_list.append(address)
                temp_list.append(voucherid['purchased_item__item_id__category__name'])
                caldistribute = VoucherTotal.objects.values('total').\
                filter(voucher_no=value['voucher'], session_id=value['session_id'])[0]
                temp_list.append(caldistribute['total'])
                amount = amount + caldistribute['total']
                transport = value['distance_estimated'] * rate['value']
                temp_list.append(int(transport))
                transport_total = transport_total + transport
                amountplustrans = caldistribute['total'] + transport
                temp_list.append(int(amountplustrans))
                amountplustransport = amountplustransport + amountplustrans
                if previous_order != value['purchase_order']:
                    temp_list.append(value['purchase_order__bill__totalplusdelivery'])
                    totalbillamount = totalbillamount +\
                    value['purchase_order__bill__totalplusdelivery']
                    taxesapplied = TaxesApplied.objects.values('tax').filter(\
                        purchase_order=value['purchase_order'])
                    for tax_val in taxesapplied:
                        temp_list.append(tax_val['tax'])
                        if flag == 1:
                            servicetaxtotal = servicetaxtotal + tax_val['tax']
                            flag = 2
                        elif flag == 2:
                            educationcesstotal = educationcesstotal +\
                            tax_val['tax']
                            flag = 3
                        else:
                            heducationcesstotal = heducationcesstotal +\
                            tax_val['tax']
                    temp_list.append(value['purchase_order__bill__grand_total'])
                    grandtotalamount = grandtotalamount +\
                    value['purchase_order__bill__grand_total']
                    temp_list.append(value['purchase_order__tds'])
                    totaltds = totaltds + value['purchase_order__tds']
                    temp_list.append(value['purchase_order__bill__amount_received'])
                    totalamountreceived = totalamountreceived +\
                    value['purchase_order__bill__amount_received']
                    temp_list.append(value['purchase_order__mode_of_payment__method'])
                    temp_list.append(value['purchase_order__cheque_dd_number'])
                    temp_list.append(value['purchase_order__cheque_dd_date'])
                result.append(temp_list)
                previous_order = value['purchase_order']
            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.suspense_register')
            return render(request,'reports/suspense_register.html',\
            {'request':request_status, 'result':result, 'back_link':back_link,
            'amount':amount, 'transport_total':int(transport_total),
            'amountplustransport':int(amountplustransport),
            'totalbillamount':totalbillamount, 'totaltds':totaltds,
            'grandtotalamount':grandtotalamount,
            'totalamountreceived':totalamountreceived,
            'servicetaxtotal':servicetaxtotal,
            'educationcesstotal':educationcesstotal,
            'heducationcesstotal':heducationcesstotal})
        else:
            form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/suspense_form.html', \
            {'form':form, 'request':request_status})
    else:
        form = DateRangeSelectionForm()
        request_status = request_notify()
        return render(request,'reports/suspense_form.html', \
        {'form':form, 'request':request_status})


@login_required
def registered_users(request):
    """
    This view is used to display the suspense registers
    Argument:Http Request
    Return:Render Suspense Register
    """
    if request.method == 'POST':
        form = DateRangeSelectionForm(request.POST)
        if form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            user = User.objects.filter(
                date_joined__range=(start_date, end_date)).values(
                'first_name', 'last_name', 'email', 'customer__telephone',
                'customer__title', 'customer__company', 'date_joined',
                'customer__address__street_address', 'customer__address__pin',
                'customer__address__district', 'customer__address__province',
                'customer__org_type__type_desc')
            result = []
            for value in user:
                temp_list = []
                temp_list.append(value['date_joined'])
                if value['first_name']:
                        name = value['first_name'] + value['last_name']
                else:
                    name = value['customer__title']
                temp_list.append(name)
                temp_list.append(value['customer__address__street_address'])
                temp_list.append(value['customer__company'])
                temp_list.append(value['customer__address__district'])
                temp_list.append(value['customer__address__pin'])
                temp_list.append(value['customer__address__province'])
                temp_list.append(value['email'])
                temp_list.append(value['customer__telephone'])
                temp_list.append(value['customer__org_type__type_desc'])
                result.append(temp_list)
            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.registered_users')
            return render(request,'reports/registeredusers_result.html',\
            {'request':request_status, 'result':result, 'back_link':back_link})
        else:
            user = User.objects.values('first_name', 'last_name', 'email',
                'customer__telephone', 'customer__title', 'customer__company',
                'customer__address__street_address', 'customer__address__pin',
                'customer__address__district', 'customer__address__province',
                'customer__org_type__type_desc', 'date_joined')
            result = []
            for value in user:
                temp_list = []
                temp_list.append(value['date_joined'])
                if value['first_name']:
                        name = value['first_name'] + value['last_name']
                else:
                    name = value['customer__title']
                temp_list.append(name)
                temp_list.append(value['customer__address__street_address'])
                temp_list.append(value['customer__company'])
                temp_list.append(value['customer__address__district'])
                temp_list.append(value['customer__address__pin'])
                temp_list.append(value['customer__address__province'])
                temp_list.append(value['email'])
                temp_list.append(value['customer__telephone'])
                temp_list.append(value['customer__org_type__type_desc'])
                result.append(temp_list)
            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.registered_users')
            return render(request,'reports/registeredusers_result.html',\
            {'request':request_status, 'result':result, 'back_link':back_link})
    else:
        form = DateRangeSelectionForm()
        request_status = request_notify()
        return render(request,'reports/registeredusers_form.html', \
        {'form':form, 'request':request_status})


@login_required
def lab_report(request):
    """
    This view is used to display the lab reports
    Argument:Http Request
    Return:Render Lab Report
    """
    if request.method == 'POST':
        form = LabReportForm(request.POST)
        date_form = DateRangeSelectionForm(request.POST)
        if form.is_valid() and date_form.is_valid():
            category = request.POST['parent_category']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            if start_date > end_date:
                error_type = "Date range error"
                error = "Start date cannot be greater than end date"
                request_status = request_notify()
                temp = {'type':error_type, 'message':error}
                return render(request, 'error_page.html', temp)

            purchase_item = PurchasedItem.objects.\
            filter(purchase_order__date_time__range=(start_date, end_date),\
                item__category__parent=category).values(\
                'purchase_order_id', 'purchase_order__date_time', 'price',
                'purchase_order__buyer__first_name',
                'purchase_order__buyer__last_name',
                'purchase_order__buyer__customer__title',
                'purchase_order__buyer__customer__company',
                'purchase_order__buyer__customer__address__street_address',
                'purchase_order__buyer__customer__address__district',
                'purchase_order__buyer__customer__address__pin',
                'purchase_order__buyer__customer__address__province',
                'purchase_order__buyer__email','purchase_order__delivery_address',\
                'purchase_order__buyer__customer__telephone',
                'voucherid__purchase_order_of_session',
                'item__category__name')
            total_amount_sum = 0
            tax_list = Surcharge.objects.all().order_by('id')
            for value in purchase_item:
                applied_tax_list = []
                for tax in tax_list:
                    try:
                        taxes_applied = TaxesApplied.objects.filter(purchase_order=
                        value['purchase_order_id'], surcharge_id=tax.id)[0]
                        applied_tax_list.append(taxes_applied.tax)
                    except:
                        applied_tax_list.append('N.A')
                    
                value['applied_tax_list'] = applied_tax_list
                
                total_tax = TaxesApplied.objects.filter(purchase_order=
                value['purchase_order_id']).aggregate(Sum('tax'))
                value['total_amount'] = total_tax['tax__sum'] + value['price']
                total_amount_sum = value['total_amount'] + total_amount_sum
            category_name = Category.objects.values('name').filter(id=category)

            total = PurchasedItem.objects.filter(purchase_order__date_time__range
                = (start_date,end_date),item__category__parent=category).\
                aggregate(Sum('price')).get('price__sum', 0.00)
            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.lab_report')
            return render(request, 'reports/lab_report.html', {'purchase_item':
                           purchase_item,'start_date':start_date, 'end_date':end_date,
                          'total_cost':total, 'category_name':category_name,\
                          'request':request_status, 'back_link':back_link,
                          'total_amount_sum':total_amount_sum, 'tax_list':tax_list})
        else:
            form = LabReportForm(request.POST)
            date_form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/lab_report_form.html', \
            {'form':form,'date_form':date_form,'request':request_status})
    else:
        form = LabReportForm()
        request_status = request_notify()
        date_form = DateRangeSelectionForm()
        return render(request,'reports/lab_report_form.html', \
        {'form':form,'date_form':date_form,'request':request_status})


@login_required
def pending_clearance_register(request):
    """
    This view is used to display the suspense pending voucher registers
    Argument:Http Request
    Return:Render Suspense Pending Voucher Register
    """
    if request.method == 'POST':
        form = DateRangeSelectionForm(request.POST)
        if form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            suspenseorder = SuspenseOrder.objects.values('voucher',\
                'session_id', 'purchase_order', 'purchase_order__date_time',\
                'purchase_order__buyer__first_name',\
                'purchase_order__buyer__last_name',\
                'purchase_order__buyer__customer__title',\
                'purchase_order__buyer__customer__address__street_address',\
                'purchase_order__buyer__customer__address__district',\
                'purchase_order__buyer__customer__address__pin',\
                'purchase_order__buyer__customer__address__province').\
            filter(is_cleared=0, purchase_order__date_time__range=(start_date,end_date))
            result = []
            for suspense in suspenseorder:
                temp = []
                temp.append(suspense['voucher'])
                temp.append(suspense['purchase_order__date_time'])
                voucherid = VoucherId.objects.values(\
                    'purchase_order_of_session').filter(\
                    voucher_no=suspense['voucher'],\
                    session_id=suspense['session_id'])[0]
                temp.append(voucherid['purchase_order_of_session'])
                if suspense['purchase_order__buyer__first_name']:
                    if suspense[\
                    'purchase_order__buyer__customer__address__pin'] == None:
                        address = suspense['purchase_order__buyer__first_name']\
                        + suspense['purchase_order__buyer__last_name']\
                        + ', ' +\
                        suspense[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__province']
                    else:
                        address = suspense['purchase_order__buyer__first_name'] +\
                        suspense['purchase_order__buyer__last_name'] +\
                        ', ' +\
                        suspense[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__province']
                else:
                    if suspense[\
                    'purchase_order__buyer__customer__address__pin'] == None:
                        address =\
                        suspense['purchase_order__buyer__customer__title']\
                        + ', ' +\
                        suspense[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__province']
                    else:
                        address =\
                        suspense['purchase_order__buyer__customer__title'] +\
                        ', ' +\
                        suspense[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        suspense[\
                        'purchase_order__buyer__customer__address__province']
                temp.append(address)
                voucherid = VoucherId.objects.values(\
                    'purchase_order__purchaseditem__item__category__name').\
                filter(voucher_no=suspense['voucher'],\
                    session_id=suspense['session_id'])[0]
                temp.append(voucherid[\
                    'purchase_order__purchaseditem__item__category__name'])
                result.append(temp)
                address = ''
            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.pending_clearance_register')
            return render(request,'reports/pending_clearance_result.html',\
            {'result':result, 'request':request_status,\
            'back_link':back_link})
        else:
            form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/pending_clearance_form.html', \
            {'form':form,'request':request_status})
    else:
        form = DateRangeSelectionForm()
        request_status = request_notify()
        return render(request,'reports/pending_clearance_form.html', \
        {'form':form,'request':request_status})


@login_required
def tada_register(request):
    """
    This view is used to display the TADA registers
    Argument:Http Request
    Return:Render TADA Register
    """
    if request.method == 'POST':
        form = DateRangeSelectionForm(request.POST)
        if form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            suspense_cleared = SuspenseClearance.objects.values('voucher_no',
                'session_id', 'clear_date').filter(
                clear_date__range=(start_date,end_date))
            result=[]
            for voucher in suspense_cleared:
                tada_check = TaDa.objects.filter(voucher_no=voucher['voucher_no'],
                session=voucher['session_id'])
                if not tada_check:
                    continue
                temp=[]
                cleared_voucher_no = SuspenseClearedRegister.objects.values(
                    'suspenseclearednumber').filter(voucher_no=voucher['voucher_no'],
                    session_id=voucher['session_id'])[0]
                temp.append(cleared_voucher_no['suspenseclearednumber'])
                temp.append(voucher['clear_date'])
                voucherid = VoucherId.objects.values('receipt_no_of_session',
                    'receipt_date',
                    'purchase_order__buyer__customer__address__street_address',
                    'purchase_order__buyer__customer__address__district',
                    'purchase_order__buyer__customer__address__pin',
                    'purchase_order__buyer__customer__address__province',
                    'purchase_order__buyer__customer__title',
                    'purchase_order__buyer__first_name',
                    'purchase_order__buyer__last_name').filter(
                    voucher_no=voucher['voucher_no'],
                    session_id=voucher['session_id'])[0]
                temp.append(voucherid['receipt_no_of_session'])
                temp.append(voucherid['receipt_date'])
                address=''
                if voucherid['purchase_order__buyer__first_name']:
                    if voucherid[\
                    'purchase_order__buyer__customer__address__pin'] == None:
                        address = voucherid['purchase_order__buyer__first_name']\
                        + voucherid['purchase_order__buyer__last_name']\
                        + ', ' +\
                        voucherid[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__province']
                    else:
                        address = voucherid['purchase_order__buyer__first_name'] +\
                        voucherid['purchase_order__buyer__last_name'] +\
                        ', ' +\
                        voucherid[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__province']
                else:
                    if voucherid[\
                    'purchase_order__buyer__customer__address__pin'] == None:
                        address =\
                        voucherid['purchase_order__buyer__customer__title']\
                        + ', ' +\
                        voucherid[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__province']
                    else:
                        address =\
                        voucherid['purchase_order__buyer__customer__title'] +\
                        ', ' +\
                        voucherid[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__province']
                temp.append(address)
                tada_object = TaDa.objects.values('testing_staff').filter(
                    voucher_no=voucher['voucher_no'],
                    session=voucher['session_id'])
                list_staff = []
                for staff in tada_object:
                    testing_staff = staff['testing_staff']
                    testing_staff_list = testing_staff.split(',')
                    for testing_staff in testing_staff_list:
                        testing_staff_details = Staff.objects.filter(\
                            code=testing_staff).values('name')[0]
                        if not testing_staff_details in list_staff:
                            list_staff.append(testing_staff_details)
                temp.append(list_staff)
                tada_amount = TaDa.objects.filter(voucher_no=voucher['voucher_no'],
                    session=voucher['session_id']).aggregate(Sum('tada_amount'))
                temp.append(tada_amount['tada_amount__sum'])
                result.append(temp)
            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.tada_register')
            return render(request,'reports/tada_register.html',\
            {'result':result, 'request':request_status,\
            'back_link':back_link})
            
        else:
            form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/tada_register_form.html', \
            {'form':form,'request':request_status})
    else:
        form = DateRangeSelectionForm()
        request_status = request_notify()
        return render(request,'reports/tada_register_form.html', \
        {'form':form,'request':request_status})


@login_required
def tada_othercharges_register(request):
    """
    This view is used to display the TADA registers
    Argument:Http Request
    Return:Render TADA Register
    """
    if request.method == 'POST':
        form = DateRangeSelectionForm(request.POST)
        if form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            suspense_cleared = SuspenseClearance.objects.values('voucher_no',
                'session_id', 'clear_date', 'boring_charge_external',
                'labour_charge', 'work_charge', 'car_taxi_charge').filter(
                clear_date__range=(start_date,end_date))
            result=[]
            for voucher in suspense_cleared:
                temp=[]
                temp.append(voucher['voucher_no'])
                cleared_voucher_no = SuspenseClearedRegister.objects.values(
                    'suspenseclearednumber').filter(voucher_no=voucher['voucher_no'],
                    session_id=voucher['session_id'])[0]
                temp.append(cleared_voucher_no['suspenseclearednumber'])
                temp.append(voucher['clear_date'])
                voucherid = VoucherId.objects.values('receipt_no_of_session',
                    'receipt_date',
                    'purchase_order__buyer__customer__address__street_address',
                    'purchase_order__buyer__customer__address__district',
                    'purchase_order__buyer__customer__address__pin',
                    'purchase_order__buyer__customer__address__province',
                    'purchase_order__buyer__customer__title',
                    'purchase_order__buyer__first_name',
                    'purchase_order__buyer__last_name').filter(
                    voucher_no=voucher['voucher_no'],
                    session_id=voucher['session_id'])[0]
                temp.append(voucherid['receipt_no_of_session'])
                temp.append(voucherid['receipt_date'])
                address=''
                if voucherid['purchase_order__buyer__first_name']:
                    if voucherid[\
                    'purchase_order__buyer__customer__address__pin'] == None:
                        address = voucherid['purchase_order__buyer__first_name']\
                        + voucherid['purchase_order__buyer__last_name']\
                        + ', ' +\
                        voucherid[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__province']
                    else:
                        address = voucherid['purchase_order__buyer__first_name'] +\
                        voucherid['purchase_order__buyer__last_name'] +\
                        ', ' +\
                        voucherid[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__province']
                else:
                    if voucherid[\
                    'purchase_order__buyer__customer__address__pin'] == None:
                        address =\
                        voucherid['purchase_order__buyer__customer__title']\
                        + ', ' +\
                        voucherid[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__province']
                    else:
                        address =\
                        voucherid['purchase_order__buyer__customer__title'] +\
                        ', ' +\
                        voucherid[\
                        'purchase_order__buyer__customer__address__street_address']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__district']\
                        + ', ' + \
                        voucherid[\
                        'purchase_order__buyer__customer__address__province']
                temp.append(address)
                tada_amount = TaDa.objects.filter(voucher_no=voucher['voucher_no'],
                    session=voucher['session_id']).aggregate(Sum('tada_amount'))
                temp.append(tada_amount['tada_amount__sum'])
                temp.append(voucher['boring_charge_external'])
                temp.append(voucher['labour_charge'])
                temp.append(voucher['car_taxi_charge'])
                try:
                    transport = Transport.objects.values('total').filter(
                        voucher_no=voucher['voucher_no'],
                        session_id=voucher['session_id'])[0]
                    transport_total = transport['total']
                except:
                    transport_total = 0
                temp.append(transport_total)
                temp.append(voucher['work_charge'])
                if tada_amount['tada_amount__sum']:
                    grand_total = int(voucher['boring_charge_external']) +\
                    int(voucher['labour_charge']) + int(transport_total) +\
                    int(tada_amount['tada_amount__sum']) + voucher['work_charge'] +\
                    voucher['car_taxi_charge']
                else:
                    grand_total = int(voucher['boring_charge_external']) +\
                    int(voucher['labour_charge']) + int(transport_total) +\
                    voucher['work_charge'] + voucher['car_taxi_charge']
                temp.append(grand_total)
                result.append(temp)
            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.tada_othercharges_register')
            return render(request,'reports/tada_othercharges.html',\
            {'result':result, 'request':request_status,\
            'back_link':back_link})
            
        else:
            form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/tada_othercharges_form.html', \
            {'form':form,'request':request_status})
    else:
        form = DateRangeSelectionForm()
        request_status = request_notify()
        return render(request,'reports/tada_othercharges_form.html', \
        {'form':form,'request':request_status})


@login_required
def client_details_according_to_amount(request):
    """
    This view is used to display the TADA registers
    Argument:Http Request
    Return:Render TADA Register
    """
    if request.method == 'POST':
        form = AmountForm(request.POST)
        if form.is_valid():
            amount = request.POST['amount']
            bill = Bill.objects.values('purchase_order').filter(amount_received__gte=amount)
            voucherid = VoucherId.objects.filter(purchase_order__in=bill).values('receipt_no_of_session',
                'receipt_date', 'purchase_order_of_session', 'session_id',
                'purchase_order__bill__amount_received',
                'purchase_order__date_time', 'purchase_order__buyer__first_name',
                'purchase_order__buyer__last_name',
                'purchase_order__buyer__customer__title',
                'purchase_order__delivery_address',
                'purchase_order__buyer__customer__address__district',
                'purchase_order__buyer__customer__address__province',
                'purchase_order__buyer__customer__address__pin',
                'purchase_order__buyer__customer__address__street_address',
                'purchase_order_id', 'session_id').distinct().order_by('session_id',
                'receipt_no_of_session')
            for value in voucherid:
                voucherid2 = VoucherId.objects.filter(purchase_order=value['purchase_order_id']
                    ).values_list('purchase_order__purchaseditem__item__category__name',
                    flat=True)
                value['material'] = voucherid2

            request_status = request_notify()
            back_link=reverse('librehatti.reports.register.client_details_according_to_amount')
            return render(request,'reports/amount_result.html',\
            {'voucherid':voucherid, 'request':request_status,\
            'back_link':back_link})
            
        else:
            form = AmountForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/amount_form.html', \
            {'form':form,'request':request_status})
    else:
        form = AmountForm()
        request_status = request_notify()
        return render(request,'reports/amount_form.html', \
        {'form':form,'request':request_status})
