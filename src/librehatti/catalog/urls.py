from django.conf.urls import url, patterns
from django.views.generic import TemplateView


urlpatterns = patterns('librehatti.catalog.views',
        url(r'^$', 'index'),
        url(r'^addCategory/','addCategories'),
)
