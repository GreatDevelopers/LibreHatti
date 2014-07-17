from django.conf.urls import url, patterns
from django.views.generic import TemplateView


urlpatterns = patterns('librehatti.prints.views',        
    url(r'^bill/', 'bill'),
)	
