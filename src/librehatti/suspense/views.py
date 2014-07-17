from django.shortcuts import render
from models import SuspenseClearance
from django.http import HttpResponse
from librehatti.catalog.models import *
from librehatti.suspense.models import *
from librehatti.suspense.forms import *
import datetime

def clearance_search(request):
    return render(request,'suspense/suspense_first.html')

def clearance(request):
    if 'Search' in request.GET:
        ref_no = request.GET['q']
        cl_report = Clearance_form(initial = {'work_charge':0, 'labour_charge':
                    0, 'car_taxi_charge':0,'boring_charge_external':0,
                    'boring_charge_internal':0,'Test_date':datetime.date.today
                    })
        temp = {'q':ref_no,'cl_report':cl_report,}
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
        Test_date= request.GET['Test_date']
        obj= SuspenseClearance(work_charge=work_charge, labour_charge=
             labour_charge, car_taxi_charge=car_taxi_charge, 
             boring_charge_external=boring_charge_external,
             boring_charge_internal=boring_charge_internal,lab_testing_staff=
             lab_testing_staff,field_testing_staff=field_testing_staff,
             Test_date=Test_date)
        obj.save()
        temp = {'ref_no': ref_no,'work_charge':work_charge ,'labour_charge':
                labour_charge, 'car_taxi_charge':car_taxi_charge,
                'boring_charge_external':boring_charge_external,
                'boring_charge_internal':boring_charge_internal,
                'lab_testing_staff':lab_testing_staff, 'field_testing_staff':
                field_testing_staff, 'Test_date':Test_date}
        return render(request, 'suspense/clearance_result.html', temp) 

def other_charges(request):
    obj = SuspenseClearance.objects.filter(id=1).values('boring_charge_external','labour_charge','car_taxi_charge')
    total = SuspenseClearance.objects.filter(id=1).aggregate(Sum('boring_charge_external','labour_charge','car_taxi_charge')) 
    return render(request,'suspense/othercharge.html',{'obj':obj,'total':total})
def withouttransport(request):
    return render(request,'suspense/withouttransport.html')

def with_transport(request):
    return render(request,'suspense/with_transport.html')

def wtransport(request):
    return render(request,'suspense/wtransport.html')

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
