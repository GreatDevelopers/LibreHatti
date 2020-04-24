# -*- coding: utf-8 -*-
from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r"^add_distance", views.add_distance, name="add_distance"),
    re_path(r"^clresult/", views.clearance_result, name="clearance_result"),
    re_path(r"^clsearch/", views.clearance_search, name="clearance_search"),
    re_path(r"^othercharges/", views.other_charges, name="other_charges"),
    re_path(r"^tada_result/", views.tada_result, name="tada_result"),
    re_path(
        r"^tada_order_session/",
        views.tada_order_session,
        name="tada_order_session",
    ),
    re_path(r"^with_transport/", views.with_transport, name="with_transport"),
    re_path(r"^transport/", views.transport, name="transport"),
    re_path(r"^transportbill/", views.transportbill, name="transportbill"),
    re_path(
        r"^quoted_add_distance",
        views.quoted_add_distance,
        name="quoted_add_distance",
    ),
    re_path(
        r"^quoted_save_distance",
        views.quoted_save_distance,
        name="quoted_save_distance",
    ),
    re_path(r"^save_distance", views.save_distance, name="save_distance"),
    re_path(r"^sessionselect/", views.sessionselect, name="sessionselect"),
    re_path(r"^mark_clear/", views.mark_clear, name="mark_clear"),
    re_path(r"^mark_status/", views.mark_status, name="mark_status"),
    re_path(
        r"^clearance_options/",
        views.clearance_options,
        name="clearance_options",
    ),
    re_path(r"^summary_page/", views.summary_page, name="summary_page"),
    re_path(r"^transport_bill/", views.transport_bill, name="transport_bill"),
    re_path(r"^tada_bill/", views.tada_bill, name="tada_bill"),
    re_path(r"^tada_bill_list/", views.tada_bill_list, name="tada_bill_list"),
    re_path(
        r"^car_taxi_advance_form/",
        views.car_taxi_advance_form,
        name="car_taxi_advance_form",
    ),
    re_path(
        r"^car_taxi_advance/", views.car_taxi_advance, name="car_taxi_advance"
    ),
]
