from django.shortcuts import render

from django.http import HttpResponse

from forms import DailyReportForm

from datetime import datetime

from librehatti.catalog.request_change import request_notify
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import Bill

from django.contrib.auth.decorators import login_required


@login_required
def daily_report_result(request):
    """
    This view is used to display the daily report registers
    """ 
    if request.method == 'POST':
        if 'button1' in request.POST:
            form = DailyReportForm(request.POST)
            if form.is_valid():
                start_date = request.POST['start_date']

                end_date = request.POST['end_date']
                #return HttpResponse(end_date)
                mode_of_payment = request.POST['Type']
                list_of_report = []

                purchase_order = PurchaseOrder.objects.filter(date_time__range=(start_date,end_date)).filter(mode_of_payment = mode_of_payment).values('date_time','id')
                #return HttpResponse(purchase_order)
                for date_value in purchase_order:
                        bill_object = Bill.objects.filter(purchase_order_id = date_value['id']).values('grand_total','purchase_order_','purchase_order__date_time','purchase_order__buyer__first_name','purchase_order__buyer__last_name','purchase_order__buyer__customer__user__customer__address__street_address','purchase_order__buyer__customer__user__customer__address__city')
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
                request_status = request_notify()
                return render(request,'reports/daily_report_form.html', \
                {'form':form,'request':request_status})
    else:
        form = DailyReportForm()
        request_status = request_notify()
        return render(request,'reports/daily_report_form.html', \
        {'form':form,'request':request_status})    