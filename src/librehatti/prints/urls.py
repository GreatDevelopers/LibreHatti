from django.conf.urls import url, patterns
from django.views.generic import TemplateView


urlpatterns = patterns('librehatti.report.views',
        
        url(r'^bill/', 'bill'),
)	
