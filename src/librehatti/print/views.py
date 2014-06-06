from django.shortcuts import render
from librehatti.catalog.models import *


def generate_bill(request):
        ORDER_NO = 3;
        order = PurchaseOrder.objects.filter(id=ORDER_NO)
        date = order.date_time.strftime('%b %d, %Y'))0
        name = order.buyer_id.first_name+order.buyer_id.last_name+
               order.buyer_id.title
