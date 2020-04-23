from django.shortcuts import render

from django.urls import reverse

from django.http import HttpResponse

from .forms import ClientForm
from .forms import OrderForm
from .forms import AddConstraints
from .forms import DailyReportForm

import simplejson

from datetime import datetime

import librehatti.settings as settings

from librehatti.catalog.request_change import request_notify
from librehatti.catalog.models import PurchaseOrder
from librehatti.catalog.models import Bill
from librehatti.catalog.models import Category

from librehatti.reports.models import SavedRegisters

from django.contrib.auth.decorators import login_required


@login_required
def search_form(request):
    """
    View to display "search.html" i.e. the search interface or form.

    First it'll check which type of request is i.e; 'search' request or
    'generate register' request. On the basis of that, it'll assign code
    to search_type_code which will be used in template.

    It'll raise an exception if anyone give invalid value in 'type'.
    Argument:Http Request
    Return:Render Search
    """
    try:
        if request.GET["type"] == "search":
            submit_url = reverse("search_result")
            search_type_code = "1"
            client_form = ClientForm()
            order_form = OrderForm()
            request_status = request_notify()
            temp = {
                "client_form": client_form,
                "order_form": order_form,
                "code": search_type_code,
                "url": submit_url,
                "request": request_status,
            }
        elif request.GET["type"] == "register":
            submit_url = reverse("view_register")
            search_type_code = "2"
            client_form = ClientForm()
            order_form = OrderForm()
            add_constraints = AddConstraints()
            request_status = request_notify()
            temp = {
                "client_form": client_form,
                "order_form": order_form,
                "add_constraints": add_constraints,
                "code": search_type_code,
                "url": submit_url,
                "request": request_status,
            }
        else:
            return HttpResponse("<h1>Page not found</h1>")
    except:
        return HttpResponse("<h1>Invalid URL</h1>")
    return render(request, "reports/search.html", temp)


@login_required
def save_fields(request):
    """
    Save generated register.
    Argument:Http Request
    """

    title = request.GET["title"]

    if title:
        pass
    else:
        return HttpResponse("0")

    selected_fields = request.META["QUERY_STRING"]

    save_fields = SavedRegisters(title=title, selected_fields=selected_fields)
    save_fields.save()
    return HttpResponse("1")


@login_required
def list_saved_registers(request):
    """
    List saved registers
    Argument:Http Request
    Return:Render List of Registers
    """
    local_url = settings.LOCAL_URL
    list_of_registers = SavedRegisters.objects.values("title", "selected_fields")
    request_status = request_notify()
    return render(
        request,
        "reports/list_of_registers.html",
        {
            "list_of_registers": list_of_registers,
            "local_url": local_url,
            "request": request_status,
        },
    )


@login_required
def filter_sub_category(request):
    """
    This view filters the sub_category according to the parent_category.
    Argument:Http Request
    Return:Http Response
    """
    parent_category = request.GET["parent_id"]
    sub_categories = Category.objects.filter(parent=parent_category)
    sub_category_dict = {}
    for sub_category in sub_categories:
        sub_category_dict[sub_category.id] = sub_category.name
    return HttpResponse(simplejson.dumps(sub_category_dict))
