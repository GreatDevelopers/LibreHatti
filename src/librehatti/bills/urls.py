from django.conf.urls import url, patterns 
from librehatti.bills import views

urlpatterns = patterns('librehatti.bills.views',
        url(r'^proforma/', 'proforma') , 
        url(r'^generateproforma/(?P<client_id>\d+)/', 'gen_proforma'),
        url(r'^confirm/(?P<client_id>\d+)/', 'confirm'),
        url(r'^confirm/final/(?P<name>\w+)/', 'final'),
        url(r'^quotation/bill/(?P<order_id>\d+)/', 'quote_table'),
        url(r'^quotation/generate/', 'generate_bill'), 
        url(r'^quoted_bill_cal/','quoted_bill_cal'),
        url(r'^quoted_order_added_success/','quoted_order_added_success')
)
