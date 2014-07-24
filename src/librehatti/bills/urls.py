from django.conf.urls import url, patterns 
from librehatti.bills import views

urlpatterns = patterns('librehatti.bills.views',
        url(r'^proforma/', 'proforma') , 
        url(r'^generateproforma/(?P<client_id>\d+)/', 'gen_proforma'),
	#url(r'^list_quoted/', 'list_quoted'),
       	#url(r'^list_quoted/confirm','confirm'),
        url(r'^confirm/(?P<client_id>\d+)/', 'confirm'),
        url(r'^confirm/final/(?P<name>\w+)/', 'final'),
       	url(r'^transport/', 'transport'),
        url(r'^transp/', 'transport_bill'),
)
