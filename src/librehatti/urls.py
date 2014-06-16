from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from librehatti.report.views import report
admin.autodiscover()


urlpatterns = patterns('',
        url(r'^$', 'librehatti.catalog.views.index'),
        url(r'^report/', 'librehatti.report.views.report'),
        url(r'^catalog/', include('librehatti.catalog.urls')),
        url(r'^useraccounts/', include('useraccounts.urls')),
        url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
