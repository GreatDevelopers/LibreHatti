from django.db import models
from librehatti.catalog.models import PurchaseOrder 
import datetime
 
class FinancialSession(models.Model):
    session_start_date = models.DateField()
    session_end_date = models.DateField()
    def __unicode__(self):
    	return "%s" % (self.id)


class VoucherId(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder)
    voucher_no = models.IntegerField()
    purchase_order_of_session = models.IntegerField()
    purchased_item_of_session = models.IntegerField()
    session = models.ForeignKey(FinancialSession)

