from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from django.shortcuts import render

from librehatti.voucher.models import VoucherId
from librehatti.voucher.models import FinancialSession
from librehatti.catalog.models import Bill
from librehatti.catalog.models import ChangeRequest
from librehatti.catalog.models import RequestSurchargeChange
from librehatti.catalog.models import RequestStatus
from librehatti.catalog.models import TaxesApplied

from librehatti.catalog.forms import ChangeRequestForm

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context

from django.contrib.auth.models import User

@login_required
def request_save(request):
    if request.method == 'POST':
        purchase_order_of_session = request.GET['order_id']
        session_id = request.GET['session']
        voucherid = VoucherId.objects.values('purchase_order_id').\
        filter(purchase_order_of_session=purchase_order_of_session, session_id=session_id)
        for value in voucherid:
            purchase_order = value['purchase_order_id']
        surcharge_list = request.POST.getlist('surcharge')
        previous_value_list = request.POST.getlist('previous_value')
        new_value_list = request.POST.getlist('new_value')
        description = request.POST.get('description')
        
        session = FinancialSession.objects.get(pk=session_id)
        bill = Bill.objects.values('grand_total').get(purchase_order_id=purchase_order)
        taxesapplied=TaxesApplied.objects.filter(purchase_order=purchase_order)


        previous_total=bill['grand_total']
        new_total=previous_total
        i=0
        for value in taxesapplied:
            if new_value_list[i]:
                new_total=int(new_total) - int(previous_value_list[i]) + int(new_value_list[i])
            else:
                pass
            i=i+1

        try:
            ChangeRequest.objects.get(purchase_order_of_session=purchase_order_of_session,\
                session=session_id)
            ChangeRequest.objects.\
            filter(purchase_order_of_session=purchase_order_of_session, session=session_id).\
            update(purchase_order_of_session=purchase_order_of_session,session = session,\
                previous_total=previous_total,new_total=new_total,description=description)
        except:
            obj= ChangeRequest(purchase_order_of_session=purchase_order_of_session,\
                session = session, previous_total=previous_total,\
                new_total=new_total,description=description)
            obj.save()


        change_request = ChangeRequest.objects.\
            get(purchase_order_of_session=purchase_order_of_session,session=session_id)
        

        i=0
        for value in taxesapplied:
            surcharge = TaxesApplied.objects.get(purchase_order=purchase_order,\
                    surcharge__tax_name=surcharge_list[i])
            if new_value_list[i]:

                if RequestSurchargeChange.objects.filter(change_request=change_request):

                    try:
                        RequestSurchargeChange.objects.get(change_request=change_request,\
                            surcharge=surcharge)
                        RequestSurchargeChange.objects.\
                        filter(change_request=change_request,surcharge=surcharge).\
                        update(change_request=change_request,\
                            surcharge=surcharge,previous_value=previous_value_list[i],\
                            new_value=new_value_list[i])
                    except:
                        obj= RequestSurchargeChange(change_request=change_request,\
                            surcharge=surcharge,previous_value=previous_value_list[i],\
                            new_value=new_value_list[i])
                        obj.save()
                else:
                    obj= RequestSurchargeChange(change_request=change_request,\
                        surcharge=surcharge,previous_value=previous_value_list[i],\
                        new_value=new_value_list[i])
                    obj.save()
            else:
                try:
                    RequestSurchargeChange.objects.\
                    get(change_request=change_request,surcharge=surcharge)
                    RequestSurchargeChange.objects.\
                    filter(change_request=change_request,surcharge=surcharge).delete()
                except:
                    pass
            i=i+1


        try:
            RequestStatus.objects.get(change_request=change_request)
            RequestStatus.objects.filter(change_request=change_request).delete()
        except:
            pass

        obj = RequestStatus(change_request=change_request)
        obj.save()

        return render(request, 'catalog/request_success.html')

    else:
        form = ChangeRequestForm()
        return render(request, 'catalog/change_request.html', \
            {'form':form})

def request_notify():
    notify = RequestStatus.objects.filter(confirmed=False).\
        filter(cancelled=False)
    if notify:
        number_request = 1
    else:
        number_request = 0
    
    return number_request

@login_required
def list_request(request):
    request_list = ChangeRequest.objects.values('id','description')
    final_request_list = []
    for value in request_list:
        if RequestStatus.objects.filter(change_request = value['id']).\
            filter(confirmed=False).filter(cancelled=False):
            request_status = 'Waiting'
        elif RequestStatus.objects.filter(change_request = value['id']).\
            filter(confirmed=True):
            request_status = 'Confirmed'
        elif RequestStatus.objects.filter(change_request = value['id']).\
            filter(cancelled=True):
            request_status = 'Cancelled'
        value['request_status'] = request_status
        final_request_list.append(value)
    return render(request, 'catalog/list_request.html',{'list':final_request_list})

@login_required
def view_request(request):
    request_id = request.GET['id']
    previous_total = ChangeRequest.objects.values('previous_total').filter(id = request_id)[0]
    new_total = ChangeRequest.objects.values('new_total').filter(id = request_id)[0]
    description = ChangeRequest.objects.values('description').filter(id = request_id)[0]
    surcharge_diff = RequestSurchargeChange.objects.values('surcharge__surcharge__tax_name',
        'previous_value','new_value').filter(change_request=request_id)
    if RequestStatus.objects.filter(change_request = request_id).\
        filter(confirmed=False).filter(cancelled=False):
        request_status = 'Waiting'
    elif RequestStatus.objects.filter(change_request = request_id).\
        filter(confirmed=True):
        request_status = 'Confirmed'
    elif RequestStatus.objects.filter(change_request = request_id).\
        filter(cancelled=True):
        request_status = 'Cancelled'
    return render(request,'catalog/view_request.html',{'previous_total':previous_total,
        'new_total':new_total,'description':description,'id':request_id,
        'surcharge_diff':surcharge_diff,'request_status':request_status})

@login_required
def accept_request(request):
    request_id = request.GET['id']
    user = User.objects.values('first_name','last_name').filter(id=request.user.id)[0]
    RequestStatus.objects.filter(id = request_id).update(confirmed=True,cancelled=False)
    previous_total = ChangeRequest.objects.values('previous_total').filter(id = request_id)[0]
    new_total = ChangeRequest.objects.values('new_total').filter(id = request_id)[0]
    description = ChangeRequest.objects.values('description').filter(id = request_id)[0]
    surcharge_diff = RequestSurchargeChange.objects.values('surcharge__surcharge__tax_name',
        'previous_value','new_value').filter(change_request=request_id)
    if RequestStatus.objects.filter(change_request = request_id).\
        filter(confirmed=False).filter(cancelled=False):
        request_status = 'Waiting'
    elif RequestStatus.objects.filter(change_request = request_id).\
        filter(confirmed=True):
        request_status = 'Confirmed'
    elif RequestStatus.objects.filter(change_request = request_id).\
        filter(cancelled=True):
        request_status = 'Cancelled'
    plaintext = get_template('catalog/response_change_email.txt')
    content = get_template('catalog/response_change_email.html')

    temp = Context({'previous_total':previous_total,'user':user,
        'new_total':new_total,'description':description,'id':request_id,
        'surcharge_diff':surcharge_diff,'request_status':request_status})

    text_content = plaintext.render(temp)
    html_content = content.render(temp)

    subject, from_email, to = 'Change Request', 'librehatti@gmail.com', 'jassigrewal91@gmail.com'

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return HttpResponse('Success')

@login_required
def reject_request(request):
    request_id = request.GET['id']
    user = User.objects.values('first_name','last_name').filter(id=request.user.id)[0]
    RequestStatus.objects.filter(id = request_id).update(cancelled=True,confirmed=False)
    previous_total = ChangeRequest.objects.values('previous_total').filter(id = request_id)[0]
    new_total = ChangeRequest.objects.values('new_total').filter(id = request_id)[0]
    description = ChangeRequest.objects.values('description').filter(id = request_id)[0]
    surcharge_diff = RequestSurchargeChange.objects.values('surcharge__surcharge__tax_name',
        'previous_value','new_value').filter(change_request=request_id)
    if RequestStatus.objects.filter(change_request = request_id).\
        filter(confirmed=False).filter(cancelled=False):
        request_status = 'Waiting'
    elif RequestStatus.objects.filter(change_request = request_id).\
        filter(confirmed=True):
        request_status = 'Confirmed'
    elif RequestStatus.objects.filter(change_request = request_id).\
        filter(cancelled=True):
        request_status = 'Cancelled'
    plaintext = get_template('catalog/response_change_email.txt')
    content = get_template('catalog/response_change_email.html')

    temp = Context({'previous_total':previous_total,'user':user,
        'new_total':new_total,'description':description,'id':request_id,
        'surcharge_diff':surcharge_diff,'request_status':request_status})

    text_content = plaintext.render(temp)
    html_content = content.render(temp)

    subject, from_email, to = 'Change Request', 'librehatti@gmail.com', 'jassigrewal91@gmail.com'

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return HttpResponse('Success')