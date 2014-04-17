from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns('librehatti.catalog.views',
	url(r'^$', 'index')
   
)
