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
        flag=0
        if 'suspense' in request.GET:
            flag=1
        temp = {'client':self.selected_fields_client,
            'order':self.selected_fields_order, 'result':generated_data_list,
            'title':self.title,'order_id':self.purchase_order_id,'records':self.results,
            'flag':flag,
            }

        return render(request,'reports/search_result.html',temp)


    def apply_filter(self,request):
        """
        Filtering according to the search term entered.
        """
        
        self.results= []
        i = 0
        buyer_id = []
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
                    self.found_entries = SuspenseOrder.objects.filter(purchase_order=self.title)
                    for entries in self.found_entries:
                        self.temp = []
                        for value in self.fields_list:
                            self.obj = SuspenseOrder.objects.values(value).\
                            filter(purchase_order=self.title)
                            for temp_result in self.obj:
                                self.temp.append(temp_result)
                        self.results.append(self.temp)
            except:
                self.found_entries = PurchaseOrder.objects.filter(id=self.title)
                for entries in self.found_entries:
                    self.temp = []
                    for value in self.fields_list:
                        self.obj = PurchaseOrder.objects.values(value).\
                        filter(id=self.title)
                        for temp_result in self.obj:
                            self.temp.append(temp_result)
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

        return self.convert_values(request)


    def fetch_values(self,request):
        """
        Fetching values from database.
        """
        if 'Client' in request.GET:
            self.details = Bill.objects.values(*self.fields_list).\
                filter(purchase_order__is_active = 1)
        elif 'Order' in request.GET:
            try:
                if request.GET['suspense']:
                    self.details = SuspenseOrder.objects.values(*self.fields_list).\
                        filter(purchase_order__is_active = 1)
            except:
                self.details = PurchaseOrder.objects.values(*self.fields_list).\
                    filter(is_active = 1)
        return self.apply_filter(request)


    def convert_values(self,request):
        """
        Mapping selected values to there names specified in 'list_dict' in this
        file.
        """

        self.fields_list = []
        if 'Order' in request.GET:
            try:
                if request.GET['suspense']:
                    self.list_dict = {'First Name':'purchase_order__buyer__first_name',
                    'Last Name':'purchase_order__buyer__last_name', 
                    'City':'purchase_order__buyer__customer__address__city',
                    'Phone':'purchase_order__buyer__customer__telephone',
                    'Joining Date':'purchase_order__buyer__customer__date_joined',
                    'Company':'purchase_order__buyer__customer__company',
                    'Discount':'purchase_order__total_discount',
                    'Debit':'purchase_order__is_debit', 
                    'Mode Of Payment':'purchase_order__mode_of_payment__method',
                    'Voucher':'voucher','Session':'session_id__id',
                    'Order Date':'purchase_order__date_time','TDS':'purchase_order__tds',
                    'Total Without Taxes':'purchase_order__bill__total_cost',
                    'Total With Taxes':'purchase_order__bill__amount_received'
                    }
            except:
                self.list_dict = {'First Name':'buyer__first_name',
                'Last Name':'buyer__last_name', 
                'City':'buyer__customer__address__city',
                'Phone':'buyer__customer__telephone',
                'Joining Date':'buyer__customer__date_joined',
                'Company':'buyer__customer__company',
                'Discount':'total_discount',
                'Debit':'is_debit', 
                'Mode Of Payment':'mode_of_payment__method',
                'Order Date':'date_time','TDS':'tds',
                'Total Without Taxes':'bill__total_cost',
                'Total With Taxes':'bill__amount_received'
                }
        for value in self.selected_fields_client:
            self.fields_list.append(self.list_dict[value])

        for value in self.selected_fields_order:
            self.fields_list.append(self.list_dict[value])
            
        if 'Client' in request.GET:
            self.fields_list.append('purchase_order__buyer__id')
        elif 'suspense' in request.GET: 
            self.fields_list.append('purchase_order__id')
        else: 
            self.fields_list.append('id')
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