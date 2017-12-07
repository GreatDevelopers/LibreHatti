from django.conf.urls import include, url

from django.views.generic import TemplateView
from . import views

urlpatterns = [
                   url(r'^add_distance', views.add_distance, name= 'add_distance'),
                   url(r'^clresult/',views.clearance_result, name= 'clearance_result'),
                   url(r'^clsearch/',views.clearance_search, name= 'clearance_search'),
                   url(r'^othercharges/',views.other_charges, name= 'other_charges'),
                   url(r'^tada_result/',views.tada_result, name= 'tada_result'),
                   url(r'^tada_order_session/',views.tada_order_session, name= 'tada_order_session'),
                   url(r'^with_transport/',views.with_transport, name= 'with_transport'),
                   url(r'^transport/',views.transport, name= 'transport'),
                   url(r'^transportbill/', views.transportbill, name= 'transportbill'),
                   url(r'^quoted_add_distance', views.quoted_add_distance, name= 'quoted_add_distance'),
                   url(r'^quoted_save_distance', views.quoted_save_distance, name= 'quoted_save_distance'),
                   url(r'^save_distance', views.save_distance, name= 'save_distance'),
                   url(r'^sessionselect/', views.sessionselect, name= 'sessionselect'),
                   url(r'^mark_clear/', views.mark_clear, name= 'mark_clear'),
                   url(r'^mark_status/', views.mark_status, name= 'mark_status'),
                   url(r'^clearance_options/', views.clearance_options, name= 'clearance_options'),
                   url(r'^summary_page/',views.summary_page, name= 'summary_page'),                   
                   url(r'^transport_bill/',views.transport_bill, name= 'transport_bill'),                   
                   url(r'^tada_bill/',views.tada_bill, name= 'tada_bill'),
                   url(r'^tada_bill_list/',views.tada_bill_list, name= 'tada_bill_list'),
                   url(r'^car_taxi_advance_form/',views.car_taxi_advance_form, name= 'car_taxi_advance_form'),
                   url(r'^car_taxi_advance/',views.car_taxi_advance, name= 'car_taxi_advance')
              ]                    
        
