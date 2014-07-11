from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('librehatti.suspense.views',
                   url(r'^$', 'suspense'),
                   url(r'^save/', 'save_charges'),
              )
