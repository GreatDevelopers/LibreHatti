# -*- coding: utf-8 -*-
"""
urls of useraccounts are..
"""
from django.contrib.auth import views as auth_views
from django.urls import path, re_path, reverse_lazy
from librehatti.catalog import views as catalog_views
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token

from . import views as useraccounts_views
from .views import CustomerSearch, CustomerView, UserList, current_user


next_page = reverse_lazy(catalog_views.index)
urlpatterns = [
    path("token-auth/", obtain_jwt_token),
    path("verify-token/", verify_jwt_token),
    path("current_user/", current_user),
    path("users/", UserList.as_view()),
    path("customer_view/", CustomerView.as_view()),
    path("customer_search/", CustomerSearch.as_view()),
    re_path(
        r"^login$",
        auth_views.LoginView,
        {"template_name": "useraccounts/login.html"},
    ),
    re_path(r"^logout$", auth_views.LogoutView, {"next_page": next_page}),
    re_path(r"^signup$", useraccounts_views.register),
]
