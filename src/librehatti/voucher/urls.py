# -*- coding: utf-8 -*-
from django.urls import re_path

from . import views


urlpatterns = [
    re_path(
        r"^voucher_generate/", views.voucher_generate, name="voucher_generate"
    ),
    re_path(r"^voucher_show/", views.voucher_show, name="voucher_show"),
    re_path(r"^voucher_print/", views.voucher_print, name="voucher_print"),
]
