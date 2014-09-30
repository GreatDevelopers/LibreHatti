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
from librehatti.catalog.models import Surcharge
from librehatti.catalog.models import TaxesApplied

from librehatti.reports.models import SavedRegisters

from django.contrib.auth.models import User

from datetime import datetime, timedelta
from calendar import monthrange

class GenerateRegister(View):

    def __init__(self):
        """
        Initializing required lists.
        """
        self.grand_total_list = []
        self.result_fields = []
        self.list_dict = {'Name':'buyer__username',
            'City':'buyer__customer__address__city',
            'Phone':'buyer__customer__telephone',
            'joining date':'buyer__customer__date_joined',
            'Company':'buyer__customer__company',
            'quantity':'qty','unit price':'item__price_per_unit',
            'item':'item__name','Discount':'total_discount',
            'Debit':'is_debit', 'total price':'price',
            'TDS': 'tds', 'Total With Taxes': 'bill__grand_total', 
            'Order Id':'id', 'Total Without Taxes': 'bill__total_cost',
            'Order Date': 'date_time',
            'Street Address': 'buyer__customer__address__street_address'
        }


    def view_register(self,request):
        """
        Converting data from dict to list form so that it can be render easily.
        Calling template to be rendered.
        """

        generated_data_list = []

        try:
            details = self.details
        except:
            details = self.client_details
        
        for data in details:
            temporary = []
            if self.surcharge:
                try:
                    data['bill__grand_total']
                except:
                    error_type = "Insufficient fields"
                    error = "Total must be included in field list"
                    temp = {'type': error_type, 'message':error}
                    return render(request,'error_page.html',temp)
            for field in self.fields_list:
                temporary.append(data[field])
            tax_pos = 0
            for val in request.GET.getlist('surcharges'):
                
                tax = TaxesApplied.objects.values_list('tax', flat = True).\
                filter(purchase_order = data['id']).filter(surcharge = val)
                try:
                    self.total_taxes[tax_pos] = self.total_taxes[tax_pos] + tax[0]
                except:
                    pass

                if tax:
                    temporary[-1:-1] = tax
                else:
                    temporary[-1:-1] = ['None']
                tax_pos = tax_pos + 1

            generated_data_list.append(temporary)
        
        number_of_fields = len(self.selected_fields_order) + len(self.\
            selected_fields_client)

        if ('Total With Taxes' in self.selected_fields_order \
            and 'Total Without Taxes' in self.selected_fields_order):
            number_of_fields -= 1
            number_of_fields = number_of_fields - self.decrement_field


        temp = {'client':self.selected_fields_client,
            'order':self.selected_fields_order, 'result':generated_data_list,
            'title':self.title, 'number_of_fields':number_of_fields,'get_data':
            self.get_data, 'save_option': self.save_option
            }

        try:
            temp['grand_total'] = self.grand_total_list
        except:
            pass 

        try:
            self.selected_fields_order[-1:-1] = self.surcharge
            temp['surcharge'] = self.surcharge
            self.grand_total_list[-1:-1]  = self.total_taxes
        except:
            pass      

        return render(request,'reports/generated_register.html',temp)

    def cal_grand_total(self,request):
        """
        Calculate grand total
        """
        grand_total = 0
        self.bill_total = 0
        self.tds = 0
        self.decrement_field = 0

        try:
            values = self.details
        except:
            values = self.client_details

        try:
            for total in values:
                if total['bill__total_cost'] is not None:
                    self.bill_total = self.bill_total + total['bill__total_cost']
            self.grand_total_list = [self.bill_total]
        except:
            pass

        try:
            for tds in values:
                if tds['tds'] is not None:
                    self.tds = self.tds + tds['tds']
            self.grand_total_list.append(self.tds)
            self.decrement_field = 1

        except:
            pass

        try:
            for total in values:
                if total['bill__grand_total'] is not None:
                    grand_total = grand_total +total['bill__grand_total']
            self.grand_total_list.append(grand_total)
        except:
            pass

        return self.view_register(request)

    def apply_filters(self,request):
        """
        Applying selected filters.
        """

        if 'date' in self.selected_fields_constraints:
            self.details = self.client_details.filter(
                date_time__range = (self.start_date,self.end_date))

        try:
            self.details = self.client_details.filter(
                mode_of_payment = self.mode_of_payment)
        except:
            pass

        try:
            month_start = str(self.year) + '-' +  str(self.month)+ '-1'
            month_end = str(self.year) + '-' +  str(self.month)+ '-' + \
                str(monthrange(int(self.year),int(self.month))[1])
            self.details = self.client_details.filter(
                date_time__range = (month_start, month_end))
        except:
            pass

        try:
            if request.GET['grand_total']:
                return self.cal_grand_total(request)

        except:
            return self.view_register(request)

    def fetch_values(self,request):
        """
        Fetching values from database.
        """
 
        try:
            try:
                if request.GET['all_registered_user']:
                    self.client_details = User.objects.values(*self.fields_list).\
                    filter(is_superuser = 0)
                    return self.view_register(request)
            except:
                self.client_details = PurchaseOrder.objects.values(*self.fields_list).\
                    filter(is_active = 1)
                return self.apply_filters(request)
        except:
            error_type = "Nothing to display"
            error = "Oops... Something went wrong."
            temp = {'type': error_type, 'message':error}
            return render(request,'error_page.html',temp)



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

        if self.fields_list:
            return self.fetch_values(request)

        else:
            self.fields_list = ['first_name','last_name', 
                'customer__address__street_address', 'customer__address__city',
                'customer__address__province']
            self.selected_fields_client = ['First Name','Last Name',
                'Street Address','City','Province']
            return self.fetch_values(request)


    def get(self,request):
        """
        Retrieve values from URL.
        Convert date into datetime format.
        """

        self.get_data = request.META['QUERY_STRING']
        self.title = request.GET['title']
        self.save_option = '1'

        saved_registers = SavedRegisters.objects.values_list('title', flat = True)

        if self.title in saved_registers:
            self.save_option = '0'

        if not self.title:
            self.title = 'General Register'

        start_date_temp = datetime.strptime(request.GET['start_date'],
            '%Y-%m-%d')
        self.start_date = datetime(start_date_temp.year, start_date_temp.month,
            start_date_temp.day) + timedelta(hours=0)

        end_date_temp = datetime.strptime(request.GET['end_date'], '%Y-%m-%d')

        #adding 24 hours in date will convert '2014-8-10' to '2014-8-10 00:00:00'

        self.end_date = datetime(end_date_temp.year, end_date_temp.month,
            end_date_temp.day) + timedelta(hours=24)

        if self.start_date > self.end_date:
            error_type = "Date range error"
            error = "Start date cannot be greater than end date"
            temp = {'type': error_type, 'message':error}
            return render(request,'error_page.html',temp)

        if request.GET.getlist('order'):
            self.selected_fields_order = request.GET.getlist('order')
            self.selected_fields_client = ['Order Id']
            self.selected_fields_client = self.selected_fields_client + request.\
                GET.getlist('client_fields')
        else:
            self.selected_fields_order = request.GET.getlist('order')
            self.selected_fields_client = request.GET.getlist('client_fields')

        self.result_fields.append(self.selected_fields_client)
        self.result_fields.append(self.selected_fields_order)
        self.selected_fields_constraints = request.GET.getlist(
            'additional_constraints')

        try:
            self.mode_of_payment = request.GET['mode_of_payment']
        except:
            pass

        try:
            self.month = request.GET['month']
        except:
            pass
        try:
            self.year = request.GET['year']
        except:
            self.year = datetime.datetime.now().strftime("%Y")
        try:
            self.surcharge = Surcharge.objects.values_list('tax_name', flat = True).\
                filter(id__in = request.GET.getlist('surcharges'))
            self.total_taxes = [0]*(len(request.GET.getlist('surcharges')))
        except:
            pass
        return self.convert_values(request)
