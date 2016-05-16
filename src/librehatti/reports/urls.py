from django.conf.urls import url, patterns

from librehatti.reports import views, register, previous_history


urlpatterns = [
    url(r'^search/',views.search_form, name='search'),
    url(r'^save_fields', views.save_fields, name='save_fields'),
    url(r'^list_saved_registers', views.list_saved_registers, name='list_saved_registers'),
    url(r'^filter_sub_category/', views.filter_sub_category, name='filter_sub_category'),
    url(r'daily_result', register.daily_report_result, name='daily_report_result'),
    url(r'consultancy_funds_report', register.consultancy_funds_report, name='consultancy_funds_report'),    
    url(r'tds_report', register.tds_report_result, name='tds_report_result'),    
    url(r'payment_report', register.payment_register, name='payment_register'),
    url(r'suspense_clearance_register', register.suspense_clearance_register, name='suspense_clearance_register'),
    url(r'servicetax', register.servicetax_register, name='servicetax'),
    url(r'^main_register', register.main_register, name='main_register'),
    url(r'^proforma_register', register.proforma_register, name='proforma_register'),
    url(r'^non_payment_register', register.non_payment_register, name='non_payment_register'),
    url(r'^client_register', register.client_register, name='client_register'),
    url(r'^material_report', register.material_report, name='material_report'),
    url(r'^lab_report', register.lab_report, name='lab_report'),
    url(r'^suspense_register', register.suspense_register, name='suspense_register'),
    url(r'^registered_users', register.registered_users, name='registered_users'),
    url(r'pending_clearance_register', register.pending_clearance_register, name='pending_clearance_register'),
    url(r'tada_register', register.tada_register, name='tada_register'),
    url(r'tada_othercharges_register', register.tada_othercharges_register, name='tada_othercharges_register'),
    url(r'client_details_according_to_amount', register.client_details_according_to_amount, name='client_details_according_to_amount'),
    url(r'^history/',previous_history.history, name='history'),
    url(r'^details/',previous_history.details, name='details'),
    url(r'^proforma_details/',previous_history.proforma_details, name='proforma_details'),
]