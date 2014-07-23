"""
%% urls.py %%

This file define the urls used in the software for suspense application. In this regular expression are used, which are used to connect the url with the functions defined.
"""
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('librehatti.suspense.views',
                   url(r'^$', 'suspense'),
                   url(r'^save/', 'save_charges'),
                   url(r'^clreport/','clearance'),
                   url(r'^clresult/','clearance_result'),
                   url(r'^clsearch/','clearance_search'),
                   url(r'^othercharges/','other_charges'),
                   url(r'^tada_form/', 'tada_form'),
                   url(r'^tada_result/','tada_result'),
                   url(r'^tada_search/','tada_search'),
                   
              )                    
        
