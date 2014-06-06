from django.shortcuts import render
from librehatti.catalog.models import *


def generateBill(request):
        orderNo = 3;
        order = purchase_order.objects.filter(id=orderNo)
        date = order.date_time.strftime('%b %d, %Y'))0
        name = order.buyer_id.first_name+order.buyer_id.last_name+
               order.buyer_id.title
