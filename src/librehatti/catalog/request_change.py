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