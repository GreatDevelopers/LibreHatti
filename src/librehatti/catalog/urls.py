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
)
