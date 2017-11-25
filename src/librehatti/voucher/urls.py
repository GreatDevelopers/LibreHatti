from django.conf.urls import url

from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^voucher_generate/',views.voucher_generate),
    url(r'^voucher_show/',views.voucher_show),
    url(r'^voucher_print/',views.voucher_print),
]
