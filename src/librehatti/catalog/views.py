from django.http import HttpResponse
from django.shortcuts import render
from librehatti.catalog.models import Category
from librehatti.catalog.models import Product
from librehatti.catalog.forms import AddCategory,TransportForm1,TransportForm2
from librehatti.catalog.models import Transport
from django.db.models import Sum
from librehatti.prints.helper import num2eng

def index(request):
    """
    It lists all the products and the user can select any product
    and can add them to the cart.
    """
    """error = {}
    categorylist = Category.objects.all()

    if categorylist.count() == 0:
        nocategory = True
        return render(request, 'catalog.html', {'nocategory': nocategory})
    productlist = Product.objects.all();

    if productlist.count() == 0:
        noproduct = True
        return render(request, 'catalog.html', {'noproduct': noproduct})

    return render(request,'catalog.html', {'productlist': productlist,
               'categorylist': categorylist})

    pass"""
    return render(request,'index.html',{})


def add_categories(request):
    """
    It allows the user to add categories.
    """

    if request.method == 'POST' :
        form = AddCategory(request.POST)
        if form.is_valid():
            return HttpResponseRedirec('/')
    else:
        form = AddCategory()
    return render(request, 'addCategory.html', {
            'form':form
    })


def transport(request):
    form = TransportFormA()
    form1 = TransportFormB()
    temp = {'TransportFormA':form, 'TransportFormB':form1}
    return render (request, 'catalog/form.html',temp)


def transport_bill(request):
    if request.method == 'POST':
        form = TransportFormA(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            vehicle_id = cd['vehicle_id']
            job_id = cd['job_id']
            kilometer = float(cd['kilometer'])
            date = request.POST['Date']
            rate = float(cd['rate'])
            total = rate * kilometer
            obj = Transport(vehicle_id=vehicle_id, job_id=job_id, 
                           kilometer=kilometer, Date=date, rate=rate, 
                           total=total) 
            obj.save()
            if 'button1' in request.POST:
                temp = Transport.objects.filter(job_id=obj.job_id)
                total_amount = Transport.objects.filter(job_id=obj.job_id
                           ).aggregate(Sum('total')).get('total__sum', 0.00)
                return render(request,'catalog/transport_bill.html', 
                           {'temp' : temp, 'words' : num2eng(total_amount), 
                            'total_amount' : total_amount}) 

            else:
                form = TransportFormB(request.POST)
                         
    else:
        form = TransportFormA()
    return render(request, 'catalog/form.html', {'TransportForm':form})         
  
