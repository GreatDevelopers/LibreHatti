from django.conf.urls import url, patterns
from django.views.generic import TemplateView

urlpatterns = patterns('librehatti.voucher.views',
    url(r'^voucher_generate/','voucher_generate'),
)
