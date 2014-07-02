from django.conf.urls import url, patterns
from librehatti.bills import views

urlpatterns = patterns('',
        url(r'^confirm/(?P<client_id>\d+)/', views.confirm, name ='confirm'),
        url(r'^confirm/final/(?P<name>\w+)/',views.final, name='final'),
)
