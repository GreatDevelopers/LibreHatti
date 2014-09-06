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
    url(r'^transport/', 'transport'),
    url(r'^transp/', 'transport_bill'),
    url(r'^jsreverse/', 'jsreverse'),
    url(r'^select_sub_category/', 'getsubcat'),
    url(r'^select_item/', 'select_item'), 
    url(r'^bill_cal/','bill_cal'),
    url(r'^list_products/','list_products'),
)
