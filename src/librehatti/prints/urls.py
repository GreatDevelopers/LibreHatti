from django.conf.urls import url, patterns

from django.views.generic import TemplateView

from librehatti.prints import views


urlpatterns = patterns('',        
    url(r'^bill/', 'bill'),
    url(r'^suspense_bill/', 'suspense_bill'),
    url(r'^quoted_bill/','quoted_bill'),
)	
