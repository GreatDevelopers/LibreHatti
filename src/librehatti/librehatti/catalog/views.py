from django.http import HttpResponse
from django.shortcuts import render
from librehatti.catalog.models import *

def index(request):
	# we have to show all products
	error = {}

	# Collect all the categories first
	categorylist = category.objects.all()
	if categorylist.count() == 0:
		nocategory = True;

	return render(request, 'catalog.html', {'nocategory': nocategory})
	pass