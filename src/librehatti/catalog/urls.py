"""
urls of catalog are..
"""
from django.conf.urls import url, patterns

"""
urls showing the list of item purchased and redirects to page of adding 
new categories of product 
"""
urlpatterns = patterns('librehatti.catalog.views',
    url(r'^$', 'index'),
    url(r'^select_sub_category/', 'select_sub_category'),
    url(r'^jsreverse/', 'jsreverse'),
    url(r'^select_item/', 'select_item'), 
    url(r'^bill_cal/','bill_cal'),
    url(r'^list_products/','list_products'),
    url(r'^previous_value/','previous_value'),
    url(r'^order_added_success/','order_added_success'),
    url(r'^change_request/','change_request'),
    url(r'^price_per_unit/','price_per_unit'),
    url(r'^select_type/','select_type'),
    url(r'^nonpaymentorderofsession/','nonpaymentorderofsession'),
    url(r'^nonpaymentordersuccess/','nonpaymentordersuccess'),
)


urlpatterns += patterns('librehatti.catalog.request_change',
   url(r'^request_save/','request_save'),
   url(r'^list_requests/','list_request'),
   url(r'^view_request/','view_request'),
   url(r'^accept_request/','accept_request'),
   url(r'^reject_request/','reject_request'),
   url(r'^permission_denied/','permission_denied'),
)