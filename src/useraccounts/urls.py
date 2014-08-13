"""
urls of useraccounts are..
"""
from django.conf.urls import patterns, url
from django.core.urlresolvers import reverse_lazy
"""
urls for the login, signup, password reset, and logout by the user
"""
next_page = reverse_lazy('librehatti.catalog.views.index')
urlpatterns = patterns('',
        (r'^login$', 'django.contrib.auth.views.login', 
        {'template_name': 'useraccounts/login.html'}),
        (r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 
        next_page}),
        (r'^signup$', 'useraccounts.views.register'),
)

