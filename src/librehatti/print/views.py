from django.shortcuts import render
from librehatti.catalog.models import *

# Create your views here.
def generateBill(request):
	orderNo = 3;
	order = purchase_order.objects.filter(id=orderNo)
	date = order.date_time.strftime('%b %d, %Y'))
	name = order.buyer_id.first_name+order.buyer_id.last_name+order.buyer_id.title
	

	
