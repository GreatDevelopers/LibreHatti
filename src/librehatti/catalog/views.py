from django.http import HttpResponse
from django.shortcuts import render
from librehatti.catalog.models import *
from librehatti.catalog.forms import *

def index(request):
	# we have to show all products
	error = {}

	# Collect all the categories first
	categorylist = category.objects.all()

	#Do we have categories
	if categorylist.count() == 0:
		nocategory = True
		return render(request, 'catalog.html', {'nocategory': nocategory})

	# Ok we have categories. Lets start showing products
	productlist = product.objects.all();

	# Do we have products
	if productlist.count() == 0:
		noproduct = True
		return render(request, 'catalog.html', {'noproduct': noproduct})

	#if none of above happens then we will do this
	return render(request,'catalog.html', {'productlist': productlist, 'categorylist': categorylist})
	pass

def addCategories(request):
	if request.method == 'POST' :
		form = addCategory(request.POST)
		if form.is_valid():
			return HttpResponseRedirec('/')
	else:
		form = addCategory()
	
	return render(request, 'addCategory.html', {
		'form':form,
	})

