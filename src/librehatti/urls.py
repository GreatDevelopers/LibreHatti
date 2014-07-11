from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
        url(r'^$', 'librehatti.catalog.views.index'),
        url(r'^suspense/', 'librehatti.suspense.views.susp'),
        url(r'^catalog/', include('librehatti.catalog.urls')),
        url(r'^useraccounts/', include('useraccounts.urls')),
        url(r'^print/', include('librehatti.print.urls')),
      	url(r'^search/','librehatti.report.search.search'),
        url(r'^search_result/','librehatti.report.views.search_result'),
	url(r'^bill/','librehatti.print.views.bill'),
        url(r'^suspense/', include('librehatti.suspense.urls')),
        url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
