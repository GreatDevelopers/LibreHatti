from django.shortcuts import render
from models import TaDa
from forms import TaDaForm
from django.db.models import Sum,Max
from django.http import HttpResponseRedirect
import datetime
from forms import TaDaSearch
from helper import num2eng

# Create your views here.

def tada_search(request):
    form = TaDaSearch
    return render( request, 'tada_search.html', { 'search_form': form })

def tada_form(request):
    ref_no = request.GET['ref_no']
    form= TaDaForm
    return render( request, 'tada_form.html', { 'form' : form, 'ref_no':ref_no } ) 
    

def tada_result(request):
    if 'Submit' in request.GET:
       #date= datetime.date.now()
       
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
       obj= TaDa(departure_time_from_tcc =departure_time_from_tcc ,arrival_time_at_site=arrival_time_at_site,
       departure_time_from_site=departure_time_from_site,arrival_time_at_tcc=arrival_time_at_tcc,
       tada_amount=tada_amount,start_test_date=start_test_date,end_test_date=end_test_date, source_site=source_site,
       testing_site=testing_site,testing_staff=testing_staff)
       obj.save()
       i=TaDa.objects.all().aggregate(Max('id'))
       j=i['id__max']
       staff = testing_staff.split(",")
       total_cost = 0
       for person in staff:
         total_cost= total_cost + int(tada_amount)
       rupees_in_words = num2eng(total_cost)
       obj1 = TaDa.objects.filter(id=j).values('departure_time_from_tcc' ,'arrival_time_at_site','departure_time_from_site','arrival_time_at_tcc', 'tada_amount','start_test_date','end_test_date','source_site', 'testing_site','testing_staff')
       #total_cost = TaDa.objects.filter(id=j).aggregate(Sum('tada_amount')).get('tada_amount__sum', 0.00)
       return render(request, 'tada_result.html', { 'obj':obj1, 'total_cost':total_cost, 'staff':staff, 'rupees_in_words':rupees_in_words })
