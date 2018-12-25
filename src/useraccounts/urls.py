"""
urls of useraccounts are..
"""
from django.conf.urls import  url
from django.urls import reverse_lazy
from django.contrib.auth import views as auth_views
from librehatti.catalog import views as catalog_views
from . import views as useraccounts_views
"""
urls for the login, signup, password reset, and logout by the user
"""
next_page = reverse_lazy(catalog_views.index)
urlpatterns = [
        url(r'^login$', auth_views.login, {'template_name': 'useraccounts/login.html'}),
        url(r'^logout$', auth_views.logout, {'next_page': next_page}),
        url(r'^signup$', useraccounts_views.register),
]

