from django.conf.urls import url, patterns

from django.views.generic import TemplateView

urlpatterns = patterns('librehatti.voucher.views',
    url(r'^voucher_generate/','voucher_generate'),
    url(r'^voucher_show/','voucher_show'),
    url(r'^voucher_print/','voucher_print'),
)
