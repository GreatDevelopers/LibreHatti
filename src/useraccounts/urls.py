# -*- coding: utf-8 -*-
"""
urls of useraccounts are..
"""
from django.contrib.auth import views as auth_views
from django.urls import re_path, reverse_lazy
from librehatti.catalog import views as catalog_views

from . import views as useraccounts_views


next_page = reverse_lazy(catalog_views.index)
urlpatterns = [
    re_path(
        r"^login$",
        auth_views.LoginView,
        {"template_name": "useraccounts/login.html"},
    ),
    re_path(r"^logout$", auth_views.LogoutView, {"next_page": next_page}),
    re_path(r"^signup$", useraccounts_views.register),
]
