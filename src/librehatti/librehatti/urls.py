from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'librehatti.catalog.views.index'),
	url(r'^catalog/', include('librehatti.catalog.urls')),
	url(r'^account/', include("registration.backends.default.urls")),
    # Examples:
    # url(r'^$', 'librehatti.views.home', name='home'),
    # url(r'^librehatti/', include('librehatti.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
