from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('librehatti.suspense.views',
                   url(r'^add_distance', 'add_distance'),
                   url(r'^clreport/','clearance'),
                   url(r'^clresult/','clearance_result'),
                   url(r'^clsearch/','clearance_search'),
                   url(r'^othercharges/','other_charges'),
                   url(r'^tada_result/','tada_result'),
                   url(r'^tada_order_session/','tada_order_session'),
                   url(r'^withouttransport/','withouttransport'),
                   url(r'^with_transport/','with_transport'),
                   url(r'^wtransport/','wtransport'),
                   url(r'^transport/', 'transport'),
                   url(r'^transportbill/', 'transportbill'),
                   url(r'^quoted_add_distance', 'quoted_add_distance'),
                   url(r'^save_distance', 'save_distance'),
                   url(r'^sessionselect/', 'sessionselect'),
                   url(r'^mark_clear/', 'mark_clear'),
                   url(r'^mark_status/', 'mark_status')

              )                    
        
