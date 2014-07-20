from django.conf.urls import url, patterns
from django.views.generic import TemplateView
from librehatti.prints import views

urlpatterns = patterns('',        
    url(r'^bill/', 'bill'),
    url(r'^add_lab/',views.add_lab, name = 'add_lab'),
    url(r'^add_material/',views.add_material, name = 'add_material'),
    url(r'^add_test', views.add_test, name= 'add_test'),
    url(r'^lab_report', views.lab_report, name= 'lab_report'),
)	
