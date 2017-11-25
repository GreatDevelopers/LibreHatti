#from django.conf.urls import patterns, include, url
from django.conf.urls import  include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from .catalog import views as catalog_views
from .reports import views as reports_views
from .prints import views as prints_views
from .programmeletter import views as programmeletter_views
from .reports.register_generator import GenerateRegister
from .reports import register
from .reports import previous_history
from .reports.search import SearchResult
from ajax_select import urls as ajax_select_urls

admin.autodiscover()
urlpatterns = [
    url(r'^$', catalog_views.index, name='home'),
    url(r'^catalog/', include('librehatti.catalog.urls')),
    url(r'^useraccounts/', include('useraccounts.urls')),
    url(r'^print/', include('librehatti.prints.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/',reports_views.search_form),
    url(r'^search_result/', SearchResult.as_view(), name='search_result'),
    url(r'^save_fields', reports_views.save_fields),
    url(r'^list_saved_registers', reports_views.list_saved_registers),
    url(r'daily_result', register.daily_report_result, name='daily_report_result'),
    url(r'consultancy_funds_report', register.consultancy_funds_report, name='consultancy_funds_report'),    
    url(r'tds_report', register.tds_report_result, name='tds_report_result'),    
    url(r'payment_report', register.payment_register, name='payment_register'),
    url(r'suspense_clearance_register', register.suspense_clearance_register),
    url(r'servicetax', register.servicetax_register),
    url(r'^main_register', register.main_register, name='main_register'),
    url(r'^proforma_register', register.proforma_register),
    url(r'^non_payment_register', register.non_payment_register),
    url(r'^client_register', register.client_register, name='client_register'),
    url(r'^material_report', register.material_report),
    url(r'^lab_report', register.lab_report),
    url(r'^suspense_register', register.suspense_register),
    url(r'^registered_users', register.registered_users),
    url(r'^filter_sub_category/', reports_views.filter_sub_category),
    url(r'^bill/', prints_views.bill),
    url(r'^suspense_bill/', prints_views.suspense_bill),
    url(r'^quoted_bill/', prints_views.quoted_bill),
    url(r'^tax/', prints_views.tax),
    url(r'^bills/', include('librehatti.bills.urls')),
    url(r'^suspense/', include('librehatti.suspense.urls')),
    url(r'^generate_register/', GenerateRegister.as_view(), name='view_register'),
    url(r'^history/',previous_history.history),
    url(r'^details/',previous_history.details),
    url(r'^proforma_details/',previous_history.proforma_details),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^voucher/', include('librehatti.voucher.urls')),
    url(r'^receipt/', prints_views.receipt),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^programmeletter/', programmeletter_views.programmeletter),
    url(r'pending_clearance_register', register.pending_clearance_register),
    url(r'tada_register', register.tada_register),
    url(r'tada_othercharges_register', register.tada_othercharges_register),
    url(r'client_details_according_to_amount', register.client_details_according_to_amount)
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
