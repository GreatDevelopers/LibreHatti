from django.shortcuts import render

from django.http import HttpResponse

from librehatti.reports.forms import DailyReportForm
from librehatti.reports.forms import ConsultancyFunds
from librehatti.reports.forms import DateRangeSelectionForm

from datetime import datetime

from librehatti.catalog.request_change import request_notify
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import Bill
from librehatti.catalog.models import PurchasedItem
from librehatti.catalog.models import Category

from django.db.models import Sum

from django.contrib.auth.decorators import login_required


@login_required
def daily_report_result(request):
    """
    This view is used to display the daily report registers
    """ 
    if request.method == 'POST':
        if 'button1' in request.POST:
            form = DailyReportForm(request.POST)
            date_form = DateRangeSelectionForm(request.POST)
            if form.is_valid() and date_form.is_valid():
                start_date = request.POST['start_date']

                end_date = request.POST['end_date']
                #return HttpResponse(end_date)
                mode_of_payment = request.POST['mode_of_payment']
                list_of_report = []

                purchase_order = PurchaseOrder.objects.filter(date_time__range=(start_date,end_date)).filter(mode_of_payment = mode_of_payment).values('date_time','id')
                #return HttpResponse(purchase_order)
                for date_value in purchase_order:
                        bill_object = Bill.objects.filter\
                        (purchase_order_id = date_value['id']).\
                        values('grand_total',\
                        'purchase_order__voucherid__purchase_order_of_session',\
                        'purchase_order__date_time',\
                        'purchase_order__buyer__first_name',\
                        'purchase_order__buyer__last_name',\
                        'purchase_order__buyer__customer__user__customer__address__street_address',\
                        'purchase_order__buyer__customer__user__customer__address__city').distinct()

                        list_of_report.append(bill_object)
                sum = 0
                for temp_var in list_of_report:
                    for total in temp_var:
                        sum = sum + total['grand_total']
                request_status = request_notify()
                return render(request,'reports/daily_report_result.html',\
                {'list_of_report':list_of_report,'sum':sum,'request':request_status})
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
        #return HttpResponse(request)
        if 'button1' in request.POST:
            form = ConsultancyFunds(request.POST)
            date_form = DateRangeSelectionForm(request.POST)
            if form.is_valid() and date_form.is_valid():
                category = request.POST['sub_category']
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                purchase_item = PurchasedItem.objects.\
                filter(purchase_order__date_time__range=(start_date, end_date),\
                	item__category=category).values\
                ('purchase_order__voucherid__purchase_order_of_session',\
                 'purchase_order__date_time',\
                 'purchase_order__buyer__first_name',\
                 'purchase_order__buyer__last_name',\
                 'purchase_order__buyer__customer__title',\
                 'purchase_order__buyer__customer__user__customer__address__street_address',\
                 'purchase_order__buyer__customer__user__customer__address__city',\
                 'purchase_order__voucherid__session_id__calculatedistribution__consultancy_asset').distinct()
                #return HttpResponse(purchase_item)
                category_name = Category.objects.filter(id=category).values('name')
                for a in category_name:
                	category_value = a['name']
                sum = PurchasedItem.objects.filter(purchase_order__date_time__range= (start_date,end_date),item__category=category).\
                aggregate(Sum('purchase_order__voucherid__session_id__calculatedistribution__consultancy_asset')).get('purchase_order__voucherid__session_id__calculatedistribution__consultancy_asset__sum', 0.00)

          #       for temp_var in purchase_item:
    	     #        sum = sum + temp_var['purchase_order__voucherid__session_id__calculatedistribution__consultancy_asset']
                #return HttpResponse(sum)
                request_status = request_notify()
                return render(request, 'reports/consultancy_funds_result.html', {'purchase_item':
    	            purchase_item,'start_date':start_date, 'end_date':end_date,
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
