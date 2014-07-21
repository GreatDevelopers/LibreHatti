from django.conf.urls import url, patterns 
from librehatti.bills import views

urlpatterns = patterns('librehatti.bills.views',
        url(r'^proforma/', 'proforma') , 
        url(r'^generateproforma/(?P<client_id>\d+)/', 'gen_proforma'),
	    url(r'^list_quoted', views.list_quoted, name ='list_quoted'),
       	url(r'^confirm/',views.confirm, name='confirm'),
       	url(r'^transport/', 'transport'),
        url(r'^transp/', 'transport_bill'),
        #url(r'^add/', 'add_another'),
)
