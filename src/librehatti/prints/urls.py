from django.conf.urls import url, patterns
from django.views.generic import TemplateView
from librehatti.prints import views

urlpatterns = patterns('',        
    url(r'^bill/', 'bill'),
    url(r'^lab_report', views.lab_report, name= 'lab_report'),
    url(r'^show_form/',views.show_form, name = 'show_form'),
    url(r'^filter_sub_category/', views.filter_sub_category,
        name = 'filter_sub_category'),
)	
