from django.shortcuts import render
from useraccounts.models import *
from librehatti.catalog.models import *
import datetime
import helper
# Create your views here.

def report(request):
    time = datetime.datetime.now()
    date = "%s %s,%s" % (time.month,time.day,time.year)
    user = Customer.objects.get(user=2)
    sum = 456
    place = user.address
    test = PurchasedItem.objects.get(item = 1)
    
    number = test.item_id
    tested_item = test.item
    sum_in_words = helper.intName(sum)
    nature_of_consistency = 'nature_of_consistency'
    val1 = 345
    val2 = 85
    val3 = 35
    val4 = val1 + val2 + val3

    return render(request,'print/report1.html',{'date':date,'nat':nature_of_consistency,'sum':sum,
    'sum_in_words':sum_in_words,'customer':user,'place':place,'test':tested_item,
    'receipt_number':number,'val1':val1,'val2':val2,'val3':val3,'val4':val4})	



