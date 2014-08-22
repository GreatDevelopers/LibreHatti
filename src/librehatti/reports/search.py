"""
%% search.py %%
This file contains the functions that will be used to generate results based on the search term entered.
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from helper import get_query

from django.shortcuts import render

from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import PurchasedItem
from librehatti.suspense.models import SuspenseOrder

from useraccounts.models import Customer

from datetime import datetime, timedelta

class SearchResult(View):

    def __init__(self):
        """
        Initializing required lists.
        """
        
        self.purchase_order_id='enable'
        self.result_fields = []
        self.list_dict = {'name':'purchase_order__buyer__username', 
            'city':'purchase_order__buyer__customer__address__city',
            'phone':'purchase_order__buyer__customer__telephone',
            'joining date':'purchase_order__buyer__customer__date_joined',
            'company':'purchase_order__buyer__customer__company',
            'discount':'purchase_order__total_discount',
            'debit':'purchase_order__is_debit', 
            'mode of payment':'purchase_order__mode_of_payment__method',
        }


    def view_results(self,request):
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
            'title':self.title,'order_id':self.purchase_order_id,'records':self.results,
            }

        return render(request,'reports/search_result.html',temp)


    def apply_filter(self,request):
        """
        Filtering according to the search term entered.
        """
        
        self.results= []
        self.entry_query= get_query(self.title,self.fields_list)
        if 'Client' in request.GET:
            self.found_entries = PurchasedItem.objects.filter(self.entry_query)
            for entries in self.found_entries:
                self.temp = []
                for value in self.fields_list:
                    obj = PurchasedItem.objects.filter(id=entries.id).values(
                            value)
                    for temp_result in obj:
                        self.temp.append(temp_result)
                self.results.append(self.temp)
                
        if 'Order' in request.GET:
            try:
                if request.GET['suspense']:
                    self.found_entries = SuspenseOrder.objects.filter(self.entry_query)
                    for entries in self.found_entries:
                        self.temp = []
                        for value in self.fields_list:
                            self.obj = SuspenseOrder.objects.filter(id=entries.id).values(value).filter(purchase_order__id=self.title)
                            for temp_result in self.obj:
                                self.temp.append(temp_result)
                        self.results.append(self.temp)
            except:
                self.found_entries = PurchasedItem.objects.filter(self.entry_query)
                for entries in self.found_entries:
                    self.temp = []
                    for value in self.fields_list:
                        self.obj = PurchasedItem.objects.filter(id=entries.id).values(value).filter(purchase_order__id=self.title)
                        for temp_result in self.obj:
                            self.temp.append(temp_result)
                    self.results.append(self.temp)

        return self.view_results(request)


    def default_fields(self,request):
        """
        Displays the default fields if no checkboxes are selected.
        """	

        if 'Client' in request.GET and not self.selected_fields_client:
            self.selected_fields_client.append('name')
            self.selected_fields_client.append('city')
		
        if 'Order' in request.GET and not self.selected_fields_order:
            self.selected_fields_client.append('name')
            self.selected_fields_client.append('city')
            self.selected_fields_order.append('debit')
            self.selected_fields_order.append('mode of payment')

        return self.convert_values(request)


    def fetch_values(self,request):
        """
        Fetching values from database.
        """

        self.details = PurchasedItem.objects.values(*self.fields_list).\
            filter(purchase_order__is_canceled = 0)

        return self.apply_filter(request)


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
        	
        if 'Client' in request.GET:
            self.fields_list.append('purchase_order__buyer__id')	
        else: 
            self.fields_list.append('purchase_order__id')
	
        return self.fetch_values(request)


    def get(self,request):
        """
        Retrieve values from URL.
        Convert date into datetime format.
        """	
        
        self.title = request.GET['search']
        self.selected_fields_client = request.GET.getlist('client_fields')
        self.selected_fields_order = request.GET.getlist('order')
        self.result_fields.append(self.selected_fields_client)
        self.result_fields.append(self.selected_fields_order)

        return self.default_fields(request)
