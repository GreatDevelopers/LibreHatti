from django.conf.urls import url, patterns
from librehatti.bills import views

urlpatterns = patterns('',
        
         url(r'^list_quoted', views.list_quoted, name ='list_quoted'),
         url(r'^confirm/',views.confirm, name='confirm'),
)        
