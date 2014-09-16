from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from reports.register_generator import GenerateRegister
from reports.search import SearchResult
from ajax_select import urls as ajax_select_urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'librehatti.catalog.views.index'),
    url(r'^catalog/', include('librehatti.catalog.urls')),
    url(r'^useraccounts/', include('useraccounts.urls')),
    url(r'^print/', include('librehatti.prints.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/','librehatti.reports.views.search_form'),
    url(r'^search_result/', SearchResult.as_view()),
    url(r'^save_fields', 'librehatti.reports.views.save_fields'),
    url(r'^list_saved_registers', 'librehatti.reports.views.list_saved_registers'),
    url(r'^bill/', 'librehatti.prints.views.bill'),
    url(r'^bills/', include('librehatti.bills.urls')),
    url(r'^suspense/', include('librehatti.suspense.urls')),
    url(r'^generate_register/', GenerateRegister.as_view()),
    url(r'^history/','librehatti.reports.previous_history.history'),
    url(r'^details/','librehatti.reports.previous_history.details'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^voucher/', include('librehatti.voucher.urls')),
    url(r'^receipt/', 'librehatti.prints.views.receipt'),
    url(r'^tinymce/', include('tinymce.urls')),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

