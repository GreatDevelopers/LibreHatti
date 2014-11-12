"""
urls of catalog are..
"""
from django.conf.urls import url, patterns
from django.views.generic import TemplateView

"""
urls showing the list of item purchased and redirects to page of adding 
new categories of product 
"""
urlpatterns = patterns('librehatti.catalog.views',
    url(r'^$', 'index'),
    url(r'^addCategory/','add_categories'),
    url(r'^select_sub_category/', 'select_sub_category'),
    url(r'^jsreverse/', 'jsreverse'),
    url(r'^select_item/', 'select_item'), 
    url(r'^bill_cal/','bill_cal'),
    url(r'^list_products/','list_products'),
    url(r'^previous_value/','previous_value'),
    url(r'^order_added_success/','order_added_success'),
)
