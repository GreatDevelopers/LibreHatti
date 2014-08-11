from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from reports.register_generator import GenerateRegister

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'librehatti.catalog.views.index'),
    url(r'^catalog/', include('librehatti.catalog.urls')),
    url(r'^useraccounts/', include('useraccounts.urls')),
    url(r'^print/', include('librehatti.prints.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', 'librehatti.reports.search.search'),
    url(r'^search_result/', 'librehatti.reports.views.search_result'),
    url(r'^bill/', 'librehatti.prints.views.bill'),
    url(r'^bills/', include('librehatti.bills.urls')),
    url(r'^suspense/', include('librehatti.suspense.urls')),
    url(r'^generate_register/', GenerateRegister.as_view()),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
