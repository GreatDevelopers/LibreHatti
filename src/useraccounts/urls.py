"""
urls of useraccounts are..
"""
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
import django.contrib.auth.views
from useraccounts import views
"""
urls for the login, signup, password reset, and logout by the user
"""
next_page = reverse_lazy('home')
urlpatterns = [
        url(r'^login/$', django.contrib.auth.views.login,
        {'template_name': 'useraccounts/login.html' },
        name='login'),
        url(r'^logout/$',django.contrib.auth.views.logout,
        {'next_page' : next_page}, name='logout'),
        url(r'^signup$', views.register, name='signup'),
]