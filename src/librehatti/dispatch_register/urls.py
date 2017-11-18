from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.dispatch_view, name='dispatch'),
]
