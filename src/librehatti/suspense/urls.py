from django.conf.urls import patterns, include, url

from django.views.generic import TemplateView

urlpatterns = patterns('librehatti.suspense.views',
                   url(r'^add_distance', 'add_distance'),
                   url(r'^clresult/','clearance_result'),
                   url(r'^clsearch/','clearance_search'),
                   url(r'^othercharges/','other_charges'),
                   url(r'^tada_result/','tada_result'),
                   url(r'^tada_order_session/','tada_order_session'),
                   url(r'^with_transport/','with_transport'),
                   url(r'^transport/', 'transport'),
                   url(r'^transportbill/', 'transportbill'),
                   url(r'^quoted_add_distance', 'quoted_add_distance'),
                   url(r'^quoted_save_distance', 'quoted_save_distance'),
                   url(r'^save_distance', 'save_distance'),
                   url(r'^sessionselect/', 'sessionselect'),
                   url(r'^mark_clear/', 'mark_clear'),
                   url(r'^mark_status/', 'mark_status'),
                   url(r'^clearance_options/', 'clearance_options'),
                   url(r'^summary_page/','summary_page'),                   
                   url(r'^transport_bill/','transport_bill'),                   
                   url(r'^tada_bill/','tada_bill'),
                   url(r'^tada_bill_list/','tada_bill_list'),
                   url(r'^car_taxi_advance_form/','car_taxi_advance_form'),
                   url(r'^car_taxi_advance/','car_taxi_advance')
              )                    
        
