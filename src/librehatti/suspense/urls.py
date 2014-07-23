from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('librehatti.suspense.views',
                   url(r'^add_distance', 'add_distance'),
                   url(r'^clreport/','clearance'),
                   url(r'^clresult/','clearance_result'),
                   url(r'^clsearch/','clearance_search'),
                   url(r'^othercharges/','other_charges'),
                   url(r'^tada_form/', 'tada_form'),
                   url(r'^tada_result/','tada_result'),
                   url(r'^tada_search/','tada_search'),
                   
              )                    
        
