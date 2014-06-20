from django.shortcuts import render
from librehatti.catalog.models import *
from forms import DeptForm
from django.http import HttpResponse
from librehatti.catalog.models import Category, PurchaseOrder,PurchasedItem


def dates(start_date, end_date):
	import datetime
	from django import forms
	if start_date > datetime.date.today() or end_date > datetime.date.today():
		raise forms.ValidationError("The date cannot be in the future!"
                      )
	elif end_date < start_date :
		raise forms.ValidationError(
                      "The start_date is greater than end_date!")
	else:
		pass 


def add_material(request):
    purchase_data = PurchaseOrder.objects.all()
    if request.method == 'POST':
        form = DeptForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            start_date = cd['start_date']
	    end_date = cd['end_date']
       	    dates(start_date, end_date)
	    purchase_data = PurchaseOrder.objects.filter(purchase_date__range
                            =(start_date,end_date)).values('buyer_id',
                            'date_time', 'organisation')
            purchase_data1 = PurchaseOrder.objects.filter(date_time__range
                             =(start_date,end_date))
            purchased_item = PurchasedItem.objects.get(buyer_id__in
                             =purchase_data1)
            sub_total= purchased_item.qty* purchased_item.price
            total_cost_temp = PurchasedItem.objects.filter(id__in=
                              purchase_data1).aggregate(Sum('sub_total'))
            total_cost = total_cost_temp['total_cost__sum']
            return HttpResponseRedirect('/print/add_material')
            return render(request, 'reports.html', {'purchase_data' :
            purchase_data, 'start_date':start_date,'end_date':end_date,
	    'total_cost':total_cost})


       
        else:
            form = DeptForm()
            material_name = Category.objects.values('name')
            return render(request,'print/form.html',{'material_name' : material_name, 
                 'form': form})



       
    
