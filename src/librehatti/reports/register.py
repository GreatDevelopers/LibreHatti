from django.shortcuts import render

from django.http import HttpResponse

from librehatti.reports.forms import DailyReportForm
from librehatti.reports.forms import ConsultancyFunds
from librehatti.reports.forms import DateRangeSelectionForm
from librehatti.reports.forms import MonthYearForm
from librehatti.reports.forms import PaidTaxesForm

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
from librehatti.catalog.models import ModeOfPayment

from librehatti.suspense.models import SuspenseOrder
from librehatti.suspense.models import Transport
from librehatti.suspense.models import TaDa
from librehatti.suspense.models import SuspenseClearance

from librehatti.voucher.models import CalculateDistribution
from librehatti.voucher.models import VoucherId
from librehatti.voucher.models import Distribution

from librehatti.bills.models import QuotedOrder
from librehatti.bills.models import QuotedOrderofSession
from librehatti.bills.models import QuotedTaxesApplied
from librehatti.bills.models import QuotedItem

from django.db.models import Sum

from django.contrib.auth.decorators import login_required


@login_required
def daily_report_result(request):
    """
    This view is used to display the daily report registers
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
                    'bill__grand_total',\
                    'voucherid__purchase_order_of_session',\
                    'buyer__first_name',\
                    'buyer__last_name',\
                    'buyer__customer__address__pin',\
                    'buyer__customer__user__customer__address__street_address',\
                    'buyer__customer__user__customer__address__city',\
                    'buyer__customer__title').distinct()
            else:
                purchase_order = PurchaseOrder.objects.filter(date_time__range=\
                     (start_date,end_date)).exclude(mode_of_payment__method=\
                     'Cash').values('date_time',\
                     'bill__grand_total',\
                     'voucherid__purchase_order_of_session',\
                     'buyer__first_name',\
                     'buyer__last_name',\
                     'buyer__customer__address__pin',\
                     'buyer__customer__user__customer__address__street_address',\
                     'buyer__customer__user__customer__address__city',\
                     'buyer__customer__title').distinct()
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
                    temp_value['buyer__customer__user__customer__address__city'])
                temp_list.append(temp_value['bill__grand_total'])
                result.append(temp_list)
                temp_list = []

            sum = 0
            for temp_var in purchase_order:
                sum = sum + temp_var['bill__grand_total']
            request_status = request_notify()
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%B-%d-%Y')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%B-%d-%Y')

            return render(request,'reports/daily_report_result.html',\
            {'result':result,'sum':sum, 'mode_name':mode_name,\
            'start_date':start_date,'end_date':end_date,\
            'request':request_status})
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
    """
    if request.method == 'POST':
        form = ConsultancyFunds(request.POST)
        date_form = DateRangeSelectionForm(request.POST)
        if form.is_valid() and date_form.is_valid():
            category = request.POST['sub_category']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            voucher_object = VoucherId.objects.\
            filter(purchase_order__date_time__range = (start_date,end_date)).\
            filter(purchased_item__item__category = category ).\
            values('purchase_order_of_session','voucher_no',\
                'session_id',\
            'purchase_order__date_time',\
            'purchase_order__buyer__first_name',\
            'purchase_order__buyer__last_name',\
            'purchase_order__buyer__customer__address__pin',\
            'purchase_order__buyer__customer__address__street_address',\
            'purchase_order__buyer__customer__address__city',\
            'purchase_order__buyer__customer__address__province',\
            'purchase_order__buyer__customer__title',\
            'purchased_item__item__category').distinct()
            temp_list = []
            result = []
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
                    temp_value['purchase_order__buyer__customer__address__city'])
                consultancy_var = CalculateDistribution.objects.values('consultancy_asset').get(voucher_no = temp_value['voucher_no'],session_id = temp_value['session_id'] )
                temp_list.append(consultancy_var['consultancy_asset'])
                result.append(temp_list)
                temp_list = []
            category_name = Category.objects.filter(id=category).values('name')
            for value in category_name:
                category_value = value['name']

            request_status = request_notify()
            start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%B-%d-%Y')
            end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%B-%d-%Y')
            return render(request, 'reports/consultancy_funds_result.html',\
             {'result':result,\
                'start_date':start_date, 'end_date':end_date,\
                'sum':sum, 'category_name':category_value,\
                'request':request_status})
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
            bill_object = Bill.objects.\
            filter(purchase_order__date_time__range=(start_date,end_date)).\
            values('purchase_order__date_time',\
            'purchase_order__id',\
            'purchase_order__buyer__first_name',\
            'purchase_order__buyer__last_name',\
            'purchase_order__buyer__customer__title',\
            'purchase_order__buyer__customer__telephone',\
            'purchase_order__buyer__customer__address__street_address',\
            'purchase_order__buyer__customer__address__city',
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
                'purchase_order__buyer__customer__address__city'])
                temp_list.append(\
                    temp_value['purchase_order__buyer__customer__telephone'])
                temp_list.append(temp_value['totalplusdelivery'])
                taxesapplied = TaxesApplied.objects.values('tax').filter(\
                purchase_order=temp_value['purchase_order__id'])
                tax_var = 0
                for taxvalue in taxesapplied:
                    temp_list.append(taxvalue['tax'])
                    if tax_var == 0:
                        service_tax = service_tax + taxvalue['tax']
                        tax_var = tax_var + 1
                    elif tax_var == 1:
                        education_tax = education_tax + taxvalue['tax']
                        tax_var = tax_var + 1
                    else:
                        heducation_tax = heducation_tax + taxvalue['tax']
                        tax_var = 0
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
            return render(request,'reports/tds_report_result.html',\
            {'result':result,'request':request_status,\
            'servicetax':servicetax,'Heducationcess':Heducationcess,\
            'educationcess':educationcess,'start_date':start_date,\
            'grandtotal':grandtotal,'end_date':end_date,\
            'billamount':billamount,'tds':tds,'amountreceived':amountreceived,\
            'surcharge_values':surcharge_values})

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
            bill_object = Bill.objects.\
            filter(purchase_order__date_time__range=(start_date,end_date)).\
            values('purchase_order__date_time',\
            'purchase_order__id',\
            'purchase_order__buyer__first_name',\
            'purchase_order__buyer__last_name',\
            'purchase_order__buyer__customer__title',\
            'purchase_order__buyer__customer__address__street_address',\
            'purchase_order__buyer__customer__address__city',
            'purchase_order__buyer__customer__address__pin',
            'totalplusdelivery','purchase_order__tds','amount_received'\
            ,'purchase_order__buyer__customer__user__email',\
            'purchase_order__buyer__customer__telephone',\
            'purchase_order__buyer__customer__company')
            #return HttpResponse(bill_object)
            servicetax = 0
            Heducationcess = 0
            educationcess = 0
            list_of_taxes = []
            for temp_value in bill_object:
                flag = 1
                voucher_object = VoucherId.objects.\
                filter(purchase_order_id = temp_value['purchase_order__id']).\
                values('purchase_order_of_session','voucher_no').distinct()
                #return HttpResponse(voucher_object)
                for value in voucher_object:
                    temp_list.append(value['purchase_order_of_session'])
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
                'purchase_order__buyer__customer__address__city'])
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
                temp_list.append(temp_value[\
                'purchase_order__buyer__customer__address__street_address'])
                temp_list.append(temp_value[\
                'purchase_order__buyer__customer__telephone'])
                temp_list.append(temp_value[\
                'purchase_order__buyer__customer__user__email'])
                temp_list.append(temp_value['totalplusdelivery'])
                for value in voucher_object:
                    taxesapplied = TaxesApplied.objects.values('tax').filter(\
                    purchase_order__voucherid__purchase_order_of_session=\
                    value['purchase_order_of_session'])
                    #return HttpResponse(taxesapplied)
                    tax_var = 0
                    for taxvalue in taxesapplied:
                        temp_list.append(taxvalue['tax'])
                        if tax_var == 0:
                            service_tax = service_tax + taxvalue['tax']
                            tax_var = tax_var + 1
                        elif tax_var == 1:
                            education_tax = education_tax + taxvalue['tax']
                            tax_var = tax_var + 1
                        else:
                            heducation_tax = heducation_tax + taxvalue['tax']
                            tax_var = 0
                temp_list.append(temp_value['purchase_order__tds'])
                temp_list.append(temp_value['amount_received'])
                result.append(temp_list)
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
            return render(request,'reports/payment_register_result.html',\
            {'result':result,'request':request_status,\
            'servicetax':servicetax,'Heducationcess':Heducationcess,\
            'educationcess':educationcess,'start_date':start_date,\
            'end_date':end_date,'billamount':billamount,\
            'tds':tds,'amountreceived':amountreceived,\
            'surcharge_values':surcharge_values})
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
                'purchase_order__buyer__customer__address__city',\
                'purchase_order__buyer__customer__address__pin',\
                'purchase_order__buyer__customer__address__province').\
            filter(is_cleared=1,\
            purchase_order__date_time__range=(start_date,end_date))
            distribution = Distribution.objects.values('college_income',\
                'admin_charges').filter()[0]
            result = []
            temp = []
            for suspense in suspenseorder:
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
                        'purchase_order__buyer__customer__address__city']\
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
                        'purchase_order__buyer__customer__address__city']\
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
                        'purchase_order__buyer__customer__address__city']\
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
                        'purchase_order__buyer__customer__address__city']\
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
                suspensecl = SuspenseClearance.objects.values(\
                    'work_charge', 'labour_charge', 'car_taxi_charge',\
                    'boring_charge_external', 'boring_charge_internal').get(\
                    voucher_no=suspense['voucher'],\
                    session_id=suspense['session_id'])
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
                temp = []
                address = ''
            request_status = request_notify()
            return render(request,'reports/suspense_clearance_result.html',\
            {'result':result, 'request':request_status,\
            'distribution':distribution})
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


@login_required
def servicetax_register(request):
    """
    This view is used to display the servicetax_register registers
    """
    if request.method == 'POST':
        form = MonthYearForm(request.POST)
        data_form = PaidTaxesForm(request.POST)
        if form.is_valid() and data_form.is_valid:
            month = request.POST['month']
            year = request.POST['year']
            service = int(request.POST['paid_service_tax'])
            education = int(request.POST['paid_education_tax'])
            highereducation = int(request.POST['paid_higher_education_tax'])
            service_tax = 0
            education_tax = 0
            heducation_tax = 0
            total = 0
            totalplustax = 0
            surcharge_list = []
            surcharge = Surcharge.objects.values('value').filter(\
                taxes_included=1)
            for sur_charge in surcharge:
                surcharge_list.append(sur_charge['value'])
            purchase_order = PurchaseOrder.objects.values('date_time', 'id',\
                'bill__totalplusdelivery', 'bill__grand_total',\
                'buyer__first_name', 'buyer__last_name',\
                'buyer__customer__title',\
                'buyer__customer__address__street_address',\
                'buyer__customer__address__city',\
                'buyer__customer__address__pin',\
                'buyer__customer__address__province').\
            filter(date_time__month=month,\
                date_time__year=year)
            temp = []
            result = []
            i=0
            for value in purchase_order:
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
                    'buyer__customer__address__city']\
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
                    'buyer__customer__address__city']\
                    + ', ' + \
                    value[\
                    'buyer__customer__address__province']
                temp.append(address)
                temp.append(value['bill__totalplusdelivery'])
                total = total+value['bill__totalplusdelivery']
                taxesapplied = TaxesApplied.objects.values('tax').filter(\
                    purchase_order=value['id'])
                for taxvalue in taxesapplied:
                    temp.append(taxvalue['tax'])
                    if i == 0:
                        service_tax = service_tax + taxvalue['tax']
                        i = i + 1
                    elif i == 1:
                        education_tax = education_tax + taxvalue['tax']
                        i = i + 1
                    else:
                        heducation_tax = heducation_tax + taxvalue['tax']
                        i = 0
                temp.append(value['bill__grand_total'])
                totalplustax = totalplustax +\
                value['bill__grand_total']
                result.append(temp)
                temp = []
                address = ''
            total_taxes = service_tax + education_tax + heducation_tax
            servicenotpaid = service_tax - service
            educationnotpaid = education_tax - education
            heducationnotpaid = heducation_tax - highereducation
            total_taxes_not_paid = servicenotpaid + educationnotpaid +\
            heducationnotpaid
            request_status = request_notify()
            month = calendar.month_name[int(month)]
            return render(request,'reports/servicetax_statement.html',\
            {'result':result, 'request':request_status, 'month':month,\
            'year':year, 'total':total, 'surcharge_list':surcharge_list,\
            'totalplustax':totalplustax, 'service_tax':service_tax,\
            'education_tax':education_tax, 'heducation_tax':heducation_tax,\
            'total_taxes':total_taxes, 'servicenotpaid':servicenotpaid,\
            'educationnotpaid':educationnotpaid, 'heducationnotpaid':\
            heducationnotpaid, 'total_taxes_not_paid':total_taxes_not_paid,\
            'service':service, 'education':education, 'highereducation':\
            highereducation})
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
                'buyer__customer__address__city',\
                'buyer__customer__address__province',\
                ).exclude(id__in = suspense_order)
            distribution = Distribution.objects.values('college_income',\
                'admin_charges').filter()[0]
            temp_list = []
            result = []
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
                        'buyer__customer__address__city']\
                        + ', ' + \
                        temp_value[\
                        'buyer__customer__address__province'])
                material = VoucherId.objects.\
                values('purchased_item__item_id__category__name').\
                filter(voucher_no = temp_value['voucherid__voucher_no'])
                for value in material:
                    temp_list.append(\
                        value['purchased_item__item_id__category__name'])
                calculated_distribution = CalculateDistribution.objects.\
                    filter(voucher_no=temp_value['voucherid__voucher_no'])\
                    .filter(session = temp_value['voucherid__session'])\
                    .values('college_income_calculated',\
                    'admin_charges_calculated',\
                    'consultancy_asset','development_fund','total')
                for value in calculated_distribution:
                    temp_list.append(value['college_income_calculated'])
                    temp_list.append(value['admin_charges_calculated'])
                    temp_list.append(value['consultancy_asset'])
                    temp_list.append(value['development_fund'])
                    temp_list.append(value['total'])
                    result.append(temp_list)
                    temp_list = []
            month_name = calendar.month_name[int(month)]
            request_status = request_notify()
            return render(request,'reports/main_register_result.html',\
            {'request':request_status, 'distribution':distribution,\
             'result':result,'month':month_name,'year':year})
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
    """
    if request.method == 'POST':
        form = DateRangeSelectionForm(request.POST)
        if form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            quotedorder = QuotedOrder.objects.values('id',\
                'quotedorderofsession__quoted_order_session', 'date_time',\
                'buyer__first_name', 'buyer__last_name',\
                'buyer__customer__title',\
                'buyer__customer__address__street_address',\
                'buyer__customer__address__city',\
                'buyer__customer__company', 'buyer__customer__telephone',\
                'buyer__email', 'quotedbill__totalplusdelivery',\
                'quotedbill__grand_total', 'delivery_address').filter(\
                date_time__range=(start_date,end_date))
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
                temp.append(order['buyer__customer__address__city'])
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
                temp.append(order['buyer__customer__telephone'])
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
            return render(request,'reports/proforma_register.html',\
            {'result':result, 'request':request_status,\
            'surcharge_values':surcharge_values})
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
    """
    if request.method == 'POST':
        form = DateRangeSelectionForm(request.POST)
        if form.is_valid():
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            non_payment_order = NonPaymentOrder.objects.values(\
                'buyer__first_name', 'buyer__last_name', 'date',\
                'buyer__customer__title', 'buyer__customer__address__pin',\
                'buyer__customer__address__street_address',\
                'buyer__customer__address__city',\
                'buyer__customer__address__province', 'reference',\
                'reference_date', 'item_type', 'delivery_address').filter(\
                date__range=(start_date,end_date))
            temp = []
            result = []
            for order in non_payment_order:
                temp.append(order['date'])
                if order['buyer__first_name']:
                    name = order['buyer__first_name'] + ' ' +\
                    order['buyer__last_name']
                else:
                    name = order['buyer__customer__title']
                temp.append(name)
                if order['buyer__customer__address__pin'] == 'None':
                    address = order['buyer__customer__address__street_address']\
                    + ', ' + order['buyer__customer__address__city'] + ', ' +\
                    order['buyer__customer__address__province']
                else:
                    address = order['buyer__customer__address__street_address']\
                    + ', ' + order['buyer__customer__address__city'] + ', ' +\
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
            return render(request,'reports/non_payment_register.html',\
            {'result':result, 'request':request_status})
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
                'buyer__customer__address__city',\
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
                        name =\
                        + temp_value['buyer__customer__title']
                    temp_list.append(name)
                    temp_list.append(\
                        temp_value['buyer__customer__address__street_address'])
                    temp_list.append(\
                        temp_value['buyer__customer__company'])
                    temp_list.append(\
                        temp_value['buyer__customer__address__city'])
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
            return render(request,'reports/client_register_result.html',\
            {'request':request_status,\
             'result':result})
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
def lab_report(request):
    """
    This view is used to display the lab reports
    """
    if request.method == 'POST':
        form = ConsultancyFunds(request.POST)
        date_form = DateRangeSelectionForm(request.POST)
        if form.is_valid() and date_form.is_valid():
            category = request.POST['sub_category']
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
                item__category=category).values(\
                'purchase_order_id', 'purchase_order__date_time', 'price',
                'purchase_order__buyer__first_name',
                'purchase_order__buyer__last_name',
                'purchase_order__buyer__customer__title',
                'purchase_order__buyer__customer__company',
                'purchase_order__buyer__customer__address__street_address',
                'purchase_order__buyer__customer__address__city',
                'purchase_order__buyer__customer__address__pin',
                'purchase_order__buyer__customer__address__province',
                'purchase_order__buyer__email','purchase_order__delivery_address',\
                'purchase_order__buyer__customer__telephone')
            category_name = Category.objects.values('name').filter(id=category)

            total = PurchasedItem.objects.filter(purchase_order__date_time__range
                = (start_date,end_date),item__category=category).\
                aggregate(Sum('price')).get('price__sum', 0.00)
            request_status = request_notify()
            return render(request, 'reports/lab_report.html', {'purchase_item':
                           purchase_item,'start_date':start_date, 'end_date':end_date,
                          'total_cost':total, 'category_name':category_name,\
                          'request':request_status})
        else:
            form = ConsultancyFunds(request.POST)
            date_form = DateRangeSelectionForm(request.POST)
            request_status = request_notify()
            return render(request,'reports/lab_report_form.html', \
            {'form':form,'date_form':date_form,'request':request_status})
    else:
        form = ConsultancyFunds()
        request_status = request_notify()
        date_form = DateRangeSelectionForm()
        return render(request,'reports/lab_report_form.html', \
        {'form':form,'date_form':date_form,'request':request_status})


@login_required
def suspense_register(request):
    """
    This view is used to display the suspense registers
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
                'purchase_order__buyer__customer__address__city',
                'purchase_order__buyer__customer__address__pin',
                'purchase_order__buyer__customer__address__province',
                'purchase_order__bill__total_cost', 'purchase_order__date_time',
                'purchase_order__bill__totalplusdelivery',
                'purchase_order__bill__grand_total', 'purchase_order__tds',
                'purchase_order__bill__amount_received',
                'purchase_order__mode_of_payment__method',
                'purchase_order__cheque_dd_number', 'purchase_order',
                'purchase_order__cheque_dd_date', 'distance_estimated')
            rate = Surcharge.objects.values('value').get(tax_name='Transportation')
            result = []
            previous_order = 0
            for value in suspenseorder:
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
                    value['buyer__last_name']
                else:
                    name = value['purchase_order__buyer__customer__title']
                temp_list.append(name)
                if value['purchase_order__buyer__customer__address__pin'] != 'None':
                    address = ', ' + \
                    value['purchase_order__buyer__customer__address__street_address'] +\
                    ', ' + value['purchase_order__buyer__customer__address__city'] +\
                    '-' + value['purchase_order__buyer__customer__address__pin'] +\
                    ', ' + value['purchase_order__buyer__customer__address__province']
                else:
                    address = ', ' + \
                    value['purchase_order__buyer__customer__address__street_address'] + \
                    ', ' + value['purchase_order__buyer__customer__address__city'] +\
                    ', ' + value['purchase_order__buyer__customer__address__province']
                temp_list.append(address)
                temp_list.append(voucherid['purchased_item__item_id__category__name'])
                caldistribute = CalculateDistribution.objects.values('total').\
                filter(voucher_no=value['voucher'], session_id=value['session_id'])[0]
                temp_list.append(caldistribute['total'])
                transport = value['distance_estimated'] * rate['value']
                temp_list.append(transport)
                amountplustrans = caldistribute['total'] + transport
                temp_list.append(amountplustrans)
                if previous_order != value['purchase_order']:
                    temp_list.append(value['purchase_order__bill__totalplusdelivery'])
                    taxesapplied = TaxesApplied.objects.values('tax').filter(\
                        purchase_order=value['purchase_order'])
                    for tax_val in taxesapplied:
                        temp_list.append(tax_val['tax'])
                    temp_list.append(value['purchase_order__bill__grand_total'])
                    temp_list.append(value['purchase_order__tds'])
                    temp_list.append(value['purchase_order__bill__amount_received'])
                    temp_list.append(value['purchase_order__mode_of_payment__method'])
                    temp_list.append(value['purchase_order__cheque_dd_number'])
                    temp_list.append(value['purchase_order__cheque_dd_date'])
                result.append(temp_list)
                previous_order = value['purchase_order']
            request_status = request_notify()
            return render(request,'reports/suspense_register.html',\
            {'request':request_status, 'result':result})
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