from django.shortcuts import render

from django.http import HttpResponse

from forms import ClientForm
from forms import OrderForm
from forms import AddConstraints
from forms import DailyReportForm


from datetime import datetime

import librehatti.settings as settings

from librehatti.catalog.request_change import request_notify
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import Bill

from librehatti.reports.models import SavedRegisters

from django.contrib.auth.decorators import login_required

@login_required
def search_form(request):
    """
    View to display "search.html" i.e. the search interface or form.
    
    First it'll check which type of request is i.e; 'search' request or 
    'generate register' request. On the basis of that, it'll assign code
    to search_type_code which will be used in template.

    It'll raise an exception if anyone give invalid value in 'type'.
    """
    try:
        if request.GET['type'] == 'search':
            submit_url = '/search_result/'
            search_type_code = '1'
            client_form = ClientForm()
            order_form = OrderForm()
            request_status = request_notify()
            temp = {'client_form':client_form,'order_form':order_form, 
            'code':search_type_code,
            'url':submit_url,
            'request':request_status    }
        elif request.GET['type'] == 'register':
            submit_url = '/generate_register/'
            search_type_code = '2'
            client_form = ClientForm()
            order_form = OrderForm()
            add_constraints=  AddConstraints()
            request_status = request_notify()
            temp = {'client_form':client_form,'order_form':order_form, 
            'add_constraints':add_constraints,'code':search_type_code,
            'url':submit_url,
            'request':request_status    }
        else:
            return HttpResponse('<h1>Page not found</h1>')
    except:
        return HttpResponse('<h1>Invalid URL</h1>')
    return render(request, 'reports/search.html',temp)


@login_required
def save_fields(request):
    """
    Save generated register.
    """

    title = request.GET['title']

    if title:
        pass
    else:
        return HttpResponse('0')

    selected_fields = request.META['QUERY_STRING']

    save_fields = SavedRegisters(title = title,\
     selected_fields = selected_fields)
    save_fields.save()
    return HttpResponse('1')


@login_required
def list_saved_registers(request):
    """
    List saved registers
    """
    local_url = settings.LOCAL_URL
    list_of_registers = SavedRegisters.objects.\
    values('title','selected_fields')
    request_status = request_notify()
    return render(request,'reports/list_of_registers.html', \
        {'list_of_registers':list_of_registers,'local_url': local_url,\
        'request':request_status})

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
                        bill_object = Bill.objects.filter(purchase_order_id = date_value['id']).values('grand_total','purchase_order_id','purchase_order__date_time','purchase_order__buyer__first_name','purchase_order__buyer__last_name','purchase_order__buyer__customer__user__customer__address__street_address','purchase_order__buyer__customer__user__customer__address__city')
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