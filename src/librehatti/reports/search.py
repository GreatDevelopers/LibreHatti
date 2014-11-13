"""
%% search.py %%
This file contains the functions that will be used to generate results based on the search term entered.
"""

from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

from helper import get_query

from django.shortcuts import render

from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import Bill
from librehatti.suspense.models import SuspenseOrder
from librehatti.voucher.models import VoucherId

from useraccounts.models import Customer

from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class SearchResult(View):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SearchResult, self).dispatch(*args, **kwargs)

    def __init__(self):
        """
        Initializing required lists.
        """
        
        self.purchase_order_id='enable'
        self.result_fields = []
        self.list_dict = {'First Name':'purchase_order__buyer__first_name',
            'Last Name':'purchase_order__buyer__last_name', 
            'City':'purchase_order__buyer__customer__address__city',
            'Street Address':'purchase_order__buyer__customer__address__street_address',
            'Phone':'purchase_order__buyer__customer__telephone',
            'Joining Date':'purchase_order__buyer__customer__date_joined',
            'Company':'purchase_order__buyer__customer__company',
            'Discount':'total_discount','Debit':'is_debit', 
            'Mode Of Payment':'mode_of_payment__method'
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
        i = 0
        buyer_id = []
        purchase_order = []
        self.entry_query= get_query(self.title,self.fields_list)
        if 'Client' in request.GET:
            self.found_entries = Bill.objects.filter(self.entry_query)
            for entries in self.found_entries:
                self.temp = []
                for value in self.fields_list:
                    obj = Bill.objects.filter(id=entries.id).values(
                            value)
                    for temp_result in obj:
                        self.temp.append(temp_result)
                if self.temp[-1] in buyer_id:
                    pass
                else:
                    buyer_id.append(self.temp[-1])
                    self.results.append(self.temp)
                
        if 'Order' in request.GET:
            try:
                if request.GET['suspense']:
                    self.found_entries = VoucherId.objects.filter(purchase_order_of_session=self.title)
                    suspenseorder = SuspenseOrder.objects.values('purchase_order_id')
                    for entries in self.found_entries:
                        self.temp = []
                        for value in self.fields_list:
                            self.obj = VoucherId.objects.values(value).\
                            filter(id=entries.id)
                            for temp_result in self.obj:
                                self.temp.append(temp_result)
                        if self.temp[-1] in suspenseorder and self.temp[-1] not in purchase_order:
                            purchase_order.append(self.temp[-1])
                            self.results.append(self.temp)
            except:
                self.found_entries = VoucherId.objects.filter(purchase_order_of_session=self.title)
                for entries in self.found_entries:
                    self.temp = []
                    for value in self.fields_list:
                        self.obj = VoucherId.objects.values(value).\
                        filter(id=entries.id)
                        for temp_result in self.obj:
                            self.temp.append(temp_result)
                    if self.temp[-1] in purchase_order:
                        pass
                    else:
                        purchase_order.append(self.temp[-1])
                        self.results.append(self.temp)

        return self.view_results(request)


    def default_fields(self,request):
        """
        Displays the default fields if no checkboxes are selected.
        """ 

        if 'Client' in request.GET and not self.selected_fields_client:
            self.selected_fields_client.append('First Name')
            self.selected_fields_client.append('Last Name')
            self.selected_fields_client.append('City')
        
        if 'Order' in request.GET and not self.selected_fields_order:
            self.selected_fields_client.append('First Name')
            self.selected_fields_client.append('Last Name')
            self.selected_fields_client.append('City')
            self.selected_fields_order.append('Debit')
            self.selected_fields_order.append('Mode Of Payment')
            self.selected_fields_order.append('Session')

        return self.convert_values(request)


    def fetch_values(self,request):
        """
        Fetching values from database.
        """
        if 'Client' in request.GET:
            self.details = Bill.objects.values(*self.fields_list).\
                filter(purchase_order__is_active = 1)
        elif 'Order' in request.GET:
            self.details = VoucherId.objects.values(*self.fields_list).\
                filter(purchase_order__is_active = 1)
        return self.apply_filter(request)


    def convert_values(self,request):
        """
        Mapping selected values to there names specified in 'list_dict' in this
        file.
        """

        self.fields_list = []
        if 'Order' in request.GET:
            self.list_dict = {'First Name':'purchase_order__buyer__first_name',
            'Last Name':'purchase_order__buyer__last_name', 
            'City':'purchase_order__buyer__customer__address__city',
            'Phone':'purchase_order__buyer__customer__telephone',
            'Joining Date':'purchase_order__buyer__customer__date_joined',
            'Company':'purchase_order__buyer__customer__company',
            'Discount':'purchase_order__total_discount',
            'Debit':'purchase_order__is_debit', 
            'Mode Of Payment':'purchase_order__mode_of_payment__method',
            'Order Date':'purchase_order__date_time','TDS':'purchase_order__tds',
            'Total Without Taxes':'purchase_order__bill__total_cost',
            'Total With Taxes':'purchase_order__bill__amount_received',
            'Session':'session_id'
            }
        for value in self.selected_fields_client:
            self.fields_list.append(self.list_dict[value])

        for value in self.selected_fields_order:
            self.fields_list.append(self.list_dict[value])
            
        if 'Client' in request.GET:
            self.fields_list.append('purchase_order__buyer__id')
        elif 'suspense' in request.GET: 
            #self.fields_list.append('session_id')
            self.fields_list.append('purchase_order_id')
        else:
            #self.fields_list.append('session_id') 
            self.fields_list.append('purchase_order_id')
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