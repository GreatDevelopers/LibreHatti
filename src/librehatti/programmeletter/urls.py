from django.conf.urls import url, patterns

from librehatti.programmeletter import views


urlpatterns = [
    url(r'^', views.programmeletter, name='programmeletter'),
]