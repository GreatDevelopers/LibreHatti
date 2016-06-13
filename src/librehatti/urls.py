from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from reports.register_generator import GenerateRegister
from reports.search import SearchResult
from ajax_select import urls as ajax_select_urls

from librehatti.catalog import views as catalog_views

admin.autodiscover()

urlpatterns = [
    url(r'^$', catalog_views.index, name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^useraccounts/', include('useraccounts.urls')),
    url(r'^catalog/', include('librehatti.catalog.urls')),
    url(r'^bills/', include('librehatti.bills.urls')),
    url(r'^print/', include('librehatti.prints.urls')),
    url(r'^programmeletter/', include('librehatti.programmeletter.urls')),
    url(r'^reports/', include('librehatti.reports.urls')),
    url(r'^suspense/', include('librehatti.suspense.urls')),
    url(r'^voucher/', include('librehatti.voucher.urls')),
    url(r'^search_result/', SearchResult.as_view(), name='search_result'),
    url(r'^generate_register/', GenerateRegister.as_view(), name='view_register'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/lookups/', include(ajax_select_urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)