# -*- coding: utf-8 -*-
"""
%% search.py %%
This file contains the functions that will be used
to generate results based on the search term entered.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import View
from librehatti.bills.models import QuotedOrderofSession
from librehatti.catalog.request_change import request_notify
from librehatti.suspense.models import SuspenseOrder
from librehatti.voucher.models import VoucherId
from useraccounts.models import User

from .helper import get_query


class SearchResult(View):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SearchResult, self).dispatch(*args, **kwargs)

    def __init__(self):
        """
        Initializing required lists.
        """
        self.purchase_order_id = "enable"
        self.result_fields = []
        self.list_dict = {
            "First Name": "first_name",
            "Last Name": "last_name",
            "district": "customer__address__district",
            "Street Address": "customer__address__street_address",
            "Phone": "customer__telephone",
            "Joining Date": "customer__date_joined",
            "Company": "customer__company",
            "Title": "customer__title",
        }

    def get(self, request):
        """
        Retrieve values from URL.
        Convert date into datetime format.
        """
        self.title = request.GET["search"]
        self.selected_fields_client = request.GET.getlist("client_fields")
        self.selected_fields_order = request.GET.getlist("order")
        self.result_fields.append(self.selected_fields_client)
        self.result_fields.append(self.selected_fields_order)
        return self.default_fields(request)

    def default_fields(self, request):
        """
        Displays the default fields if no checkboxes are selected.
        """
        if "Client" in request.GET and not self.selected_fields_client:
            self.selected_fields_client.append("First Name")
            self.selected_fields_client.append("Last Name")
            self.selected_fields_client.append("Title")
            self.selected_fields_client.append("district")
        if "Order" in request.GET and not self.selected_fields_order:
            self.selected_fields_client.append("First Name")
            self.selected_fields_client.append("Last Name")
            self.selected_fields_client.append("district")
            self.selected_fields_order.append("Debit")
            if "proforma" not in request.GET:
                self.selected_fields_order.append("Mode Of Payment")
            self.selected_fields_order.append("Session")
        return self.convert_values(request)

    def convert_values(self, request):
        """
        Mapping selected values to there names specified in 'list_dict'
        in this file.
        """
        self.fields_list = []
        if "Order" in request.GET and "proforma" not in request.GET:
            self.list_dict = {
                "First Name": "purchase_order__buyer__first_name",
                "Last Name": "purchase_order__buyer__last_name",
                "district": "purchase_order__buyer__customer__address__district",  # noqa
                "Phone": "purchase_order__buyer__customer__telephone",
                "Joining Date": "purchase_order__buyer__customer__date_joined",
                "Company": "purchase_order__buyer__customer__company",
                "Discount": "purchase_order__total_discount",
                "Debit": "purchase_order__is_debit",
                "Mode Of Payment": "purchase_order__mode_of_payment__method",
                "Order Date": "purchase_order__date_time",
                "TDS": "purchase_order__tds",
                "Total Without Taxes": "purchase_order__bill__total_cost",
                "Total With Taxes": "purchase_order__bill__amount_received",
                "Session": "session_id",
            }
        elif "Order" in request.GET and "proforma" in request.GET:
            self.list_dict = {
                "First Name": "quoted_order__buyer__first_name",
                "Last Name": "quoted_order__buyer__last_name",
                "district": "quoted_order__buyer__customer__address__district",
                "Phone": "quoted_order__buyer__customer__telephone",
                "Joining Date": "quoted_order__buyer__customer__date_joined",
                "Company": "quoted_order__buyer__customer__company",
                "Discount": "quoted_order__total_discount",
                "Debit": "quoted_order__is_debit",
                "Order Date": "quoted_order__date_time",
                "Total Without Taxes": "quoted_order__quotedbill__total_cost",
                "Total With Taxes": "quoted_order__quotedbill__amount_received",
                "Session": "session_id",
            }
        for value in self.selected_fields_client:
            self.fields_list.append(self.list_dict[value])
        for value in self.selected_fields_order:
            self.fields_list.append(self.list_dict[value])
        if "Client" in request.GET:
            self.fields_list.append("id")
        elif "proforma" in request.GET:
            self.fields_list.append("quoted_order_id")
        else:
            self.fields_list.append("purchase_order_id")
        return self.fetch_values(request)

    def fetch_values(self, request):
        """
        Fetching values from database.
        """
        if "Client" in request.GET:
            self.details = User.objects.values(*self.fields_list).all()
        elif "Order" in request.GET and "proforma" not in request.GET:
            self.details = VoucherId.objects.values(*self.fields_list).filter(
                purchase_order__is_active=1
            )
        elif "Order" in request.GET and "proforma" in request.GET:
            self.details = QuotedOrderofSession.objects.values(
                *self.fields_list
            ).filter(quoted_order__is_active=1)
        return self.apply_filter(request)

    def apply_filter(self, request):
        """
        Filtering according to the search term entered.
        """
        self.results = []
        purchase_order = []
        self.entry_query = get_query(self.title, self.fields_list)
        if "Client" in request.GET:
            self.found_entries = User.objects.filter(self.entry_query)
            for entries in self.found_entries:
                self.temp = []
                for value in self.fields_list:
                    obj = User.objects.filter(id=entries.id).values(value)
                    for temp_result in obj:
                        self.temp.append(temp_result)
                self.results.append(self.temp)
        if "Order" in request.GET:
            if "suspense" in request.GET:
                self.found_entries = VoucherId.objects.filter(
                    purchase_order_of_session=self.title
                )
                suspenseorder = SuspenseOrder.objects.values(
                    "purchase_order_id"
                )
                for entries in self.found_entries:
                    self.temp = []
                    for value in self.fields_list:
                        self.obj = VoucherId.objects.values(value).filter(
                            id=entries.id
                        )
                        for temp_result in self.obj:
                            self.temp.append(temp_result)
                    if (
                        self.temp[-1] in suspenseorder
                        and self.temp[-1] not in purchase_order
                    ):
                        purchase_order.append(self.temp[-1])
                        self.results.append(self.temp)
            elif "proforma" in request.GET:
                self.found_entries = QuotedOrderofSession.objects.filter(
                    quoted_order_session=self.title
                )
                for entries in self.found_entries:
                    self.temp = []
                    for value in self.fields_list:
                        self.obj = QuotedOrderofSession.objects.values(
                            value
                        ).filter(id=entries.id)
                        for temp_result in self.obj:
                            self.temp.append(temp_result)
                    self.results.append(self.temp)
            else:
                self.found_entries = VoucherId.objects.filter(
                    purchase_order_of_session=self.title
                )
                for entries in self.found_entries:
                    self.temp = []
                    for value in self.fields_list:
                        self.obj = VoucherId.objects.values(value).filter(
                            id=entries.id
                        )
                        for temp_result in self.obj:
                            self.temp.append(temp_result)
                    if self.temp[-1] in purchase_order:
                        pass
                    else:
                        purchase_order.append(self.temp[-1])
                        self.results.append(self.temp)
        return self.view_results(request)

    def view_results(self, request):
        """
        Converting data from dict to list form so that it can be render
        easily.
        Calling template to be rendered.
        Argument:Http Request
        Return:Render Search Result
        """
        generated_data_list = []
        for data in self.details:
            temporary = []
            for field in self.fields_list:
                temporary.append(data[field])
            generated_data_list.append(temporary)
        flag = 0
        suspense_flag = 0
        if "proforma" in request.GET:
            flag = 1
        if "Client" not in request.GET and "proforma" not in request.GET:
            try:
                voucherid = VoucherId.objects.values("purchase_order").filter(
                    purchase_order_of_session=self.title
                )[0]
                suspense = SuspenseOrder.objects.filter(
                    purchase_order=voucherid["purchase_order"]
                )
                if suspense:
                    suspense_flag = 1
            except BaseException:
                pass
        request_status = request_notify()
        temp = {
            "client": self.selected_fields_client,
            "order": self.selected_fields_order,
            "result": generated_data_list,
            "title": self.title,
            "order_id": self.purchase_order_id,
            "records": self.results,
            "request": request_status,
            "flag": flag,
            "suspense_flag": suspense_flag,
        }
        return render(request, "reports/search_result.html", temp)
