from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from librehatti.suspense import views
admin.autodiscover()


urlpatterns = patterns('',
            url(r'^tada_form/', views.tada_form,name='tada_form'),
            url(r'^tada_result/', views.tada_result,name='tada_result'),
            url(r'^tada_search/', views.tada_search,name='tada_search'),
            )
