from django.conf.urls import url

from django.views.generic import TemplateView

from librehatti.prints import views


urlpatterns = [        
    url(r'^bill/', views.bill),
    url(r'^suspense_bill/', views.suspense_bill),
    url(r'^quoted_bill/',views.quoted_bill),
]	
