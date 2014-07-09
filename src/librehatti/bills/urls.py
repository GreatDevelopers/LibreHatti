from django.conf.urls import url, patterns 


urlpatterns = patterns('librehatti.bills.views',
        url(r'^proforma/', 'proforma') , 
        url(r'^generateproforma/(?P<client_id>\d+)/', 'gen_proforma'),

)
