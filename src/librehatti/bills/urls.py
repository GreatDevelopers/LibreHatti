from django.conf.urls import url, patterns 
from librehatti.bills import views

urlpatterns = patterns('librehatti.bills.views',
        url(r'^quoted_bill_cal/','quoted_bill_cal'),
        url(r'^quoted_order_added_success/','quoted_order_added_success')
)
