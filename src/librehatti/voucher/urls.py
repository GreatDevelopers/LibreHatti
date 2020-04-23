from django.urls import re_path

from django.views.generic import TemplateView
from . import views

urlpatterns = [
    re_path(r"^voucher_generate/", views.voucher_generate, name="voucher_generate"),
    re_path(r"^voucher_show/", views.voucher_show, name="voucher_show"),
    re_path(r"^voucher_print/", views.voucher_print, name="voucher_print"),
]
