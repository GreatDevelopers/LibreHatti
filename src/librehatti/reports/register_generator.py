"""
%% actions.py %%
This file contains the functions that will be used to generate registers.
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from helper import get_query

from django.shortcuts import render

from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem

from useraccounts.models import Customer

from datetime import datetime, timedelta

class GenerateRegister(View):

    def __init__(self):
        """
        Initializing required lists.
        """

    	self.result_fields = []
        self.list_dict = {'name':'purchase_order__buyer__username', 
            'city':'purchase_order__buyer__customer__address__city',
            'phone':'purchase_order__buyer__customer__telephone',
            'joining date':'purchase_order__buyer__customer__date_joined',
            'company':'purchase_order__buyer__customer__company',
            'quantity':'qty','unit price':'item__price_per_unit',
            'item':'item__name','discount':'purchase_order__total_discount',
            'debit':'purchase_order__is_debit', 'total price':'price'
        }


    def view_register(self,request):
        """
        Converting data from dict to list form so that it can be render easily.
        Calling template to be rendered.
        """

    	generated_data_list = []

        for data in self.details:
        	temporary = []
        	for field in self.fields_list:
        		temporary.append(data[field])
        	generated_data_list.append(temporary)

        temp = {'client':self.selected_fields_client,
            'order':self.selected_fields_order, 'result':generated_data_list,
            'title':self.title
        }

        return render(request,'reports/generated_register.html',temp)

    def apply_filters(self,request):
        """
        Applying selected filters.
        """

        if 'date' in self.selected_fields_constraints:
            self.details = self.client_details.filter(
            	purchase_order__date_time__range = (
            		self.start_date,self.end_date))

        return self.view_register(request)

    def fetch_values(self,request):
        """
        Fetching values from database.
        """

    	self.details = PurchasedItem.objects.values(*self.fields_list).\
    	    filter(purchase_order__is_canceled = 0)

        return self.apply_filters(request)


    def convert_values(self,request):
        """
        Mapping selected values to there names specified in 'list_dict' in this
        file.
        """

    	self.fields_list = []
    	for value in self.selected_fields_client:
    		self.fields_list.append(self.list_dict[value])

        for value in self.selected_fields_order:
        	self.fields_list.append(self.list_dict[value])

        return self.fetch_values(request)


    def get(self,request):
        """
        Retrieve values from URL.
        Convert date into datetime format.
        """

    	self.title = request.GET['title']

    	start_date_temp = datetime.strptime(request.GET['start_date'],
    		'%Y-%m-%d')
    	self.start_date = datetime(start_date_temp.year, start_date_temp.month, 
    		start_date_temp.day) + timedelta(hours=0) 

    	end_date_temp = datetime.strptime(request.GET['end_date'], '%Y-%m-%d')

        #adding 24 hours in date will convert '2014-8-10' to '2014-8-10 00:00:00'
    	
        self.end_date = datetime(end_date_temp.year, end_date_temp.month, 
    		end_date_temp.day) + timedelta(hours=24) 

        self.selected_fields_client = request.GET.getlist('client_fields')
        self.selected_fields_order = request.GET.getlist('order')
        self.selected_fields_constraints = request.GET.getlist(
        	'additional_constraints')
        self.result_fields.append(self.selected_fields_client)
        self.result_fields.append(self.selected_fields_order)

        return self.convert_values(request)

