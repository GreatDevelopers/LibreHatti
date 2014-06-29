from django.shortcuts import render
from librehatti.catalog.models import *
from librehatti.bills.models import *
from django.contrib.auth.models import User
import useraccounts


def proforma(request):
    QuotedOrder_list = QuotedOrder.objects.all()
    QuotedItem_list = QuotedItem.objects.all()
    return render(request, 'bills/quote.html', 
                 {'QuotedOrder_list' : QuotedOrder_list, 'QuotedItem_list' : QuotedItem_list})
