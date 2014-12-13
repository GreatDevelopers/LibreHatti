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
                   url(r'^without_other_charges/','without_other_charges'),
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
                   #url(r'^print_transport_bill/','print_transport_bill'),
              )                    
        
