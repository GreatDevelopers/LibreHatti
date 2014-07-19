from django.db import models
import useraccounts
from librehatti.catalog.models import *
from django.contrib.auth.models import User


class QuotedOrder(models.Model):
    quote_buyer_id = models.ForeignKey(User)
    quote_is_debit = models.BooleanField()
    quote_delivery_address = models.ForeignKey('useraccounts.Address')
    quote_organisation = models.ForeignKey('useraccounts.AdminOrganisations')
    quote_date_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return '%s' % (self.quote_buyer_id) +' - ' '%s' % (
                       self.quote_date_time.strftime ('%b %d, %Y'))


class QuotedItem(models.Model):
    quote_order = models.ForeignKey(QuotedOrder)
    quote_price = models.IntegerField()
    quote_qty = models.IntegerField()
    quote_discount= models.IntegerField(default = 0)
    quote_item = models.ForeignKey(Product)
    confirm_status = models.IntegerField(default=0)
    def save(self):
        if not self.id:
            self.quote_price = self.quote_item.price_per_unit * self.quote_qty
        super(QuotedItem,self).save()

    def __unicode__(self):
        return '%s' % (self.quote_item) + ' - ' '%s' % (self.quote_order)


class Transport(models.Model):
    vehicle_id = models.CharField(max_length=20)
    job_id = models.IntegerField()
    kilometer = models.FloatField()
    rate = models.FloatField(default=10.0)  
    Date = models.DateField(blank=True)
    total = models.IntegerField()
    def __unicode__(self):
        return '%s' % (self.vehicle_id)

