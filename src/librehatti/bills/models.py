from django.db import models
import useraccounts
from librehatti.catalog.models import Product
from librehatti.catalog.models import ModeOfPayment
from librehatti.catalog.models import Surcharge
from django.contrib.auth.models import User


class QuotedOrder(models.Model):
    buyer_id = models.ForeignKey(User)
    is_debit = models.BooleanField(default = False)
    delivery_address = models.ForeignKey('useraccounts.Address')
    organisation = models.ForeignKey('useraccounts.AdminOrganisations')
    date_time = models.DateTimeField(auto_now_add=True)
    total_discount = models.IntegerField()
    tds = models.IntegerField()
    mode_of_payment = models.ForeignKey(ModeOfPayment)
    is_active = models.BooleanField(default=True)
    confirm_status = models.BooleanField(default=False)
    def __unicode__(self):
        return '%s' % (self.id)


class QuotedItem(models.Model):
    quote_order = models.ForeignKey(QuotedOrder)
    price = models.IntegerField(default = 0)
    qty = models.IntegerField()
    item = models.ForeignKey(Product)
    def save(self):
        if not self.id:
            self.price = self.item.price_per_unit * self.qty
        super(QuotedItem,self).save()

    def __unicode__(self):
        return '%s' % (self.item) + ' - ' '%s' % (self.quote_order)

 
class QuoteTaxesApplied(models.Model):
    quote_order = models.ForeignKey(QuotedOrder)
    surcharge = models.ForeignKey(Surcharge)
    tax = models.IntegerField()


class QuotedBill(models.Model):
    quote_order = models.ForeignKey(QuotedOrder)
    total_cost = models.IntegerField()
    total_tax = models.IntegerField()
    grand_total = models.IntegerField()
   
