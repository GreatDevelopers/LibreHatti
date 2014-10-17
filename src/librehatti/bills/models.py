from django.db import models
import useraccounts
from librehatti.catalog.models import Product
from librehatti.catalog.models import ModeOfPayment
from librehatti.catalog.models import Surcharge
from django.contrib.auth.models import User


class QuotedOrder(models.Model):
<<<<<<< HEAD
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
=======
    buyer_id = models.ForeignKey(User, verbose_name='BUYER_ID')
    is_debit = models.BooleanField(default = False)
    delivery_address = models.ForeignKey('useraccounts.Address', verbose_name='_DELIVERY_ADDRESS')
    organisation = models.ForeignKey('useraccounts.AdminOrganisations', verbose_name='_ORGANISATION')
    date_time = models.DateTimeField(auto_now_add=True)
    total_discount = models.IntegerField()
    tds = models.IntegerField()
    mode_of_payment = models.ForeignKey(ModeOfPayment, verbose_name='_MODE_OF_PAYMENT')
    is_active = models.BooleanField(default=True, verbose_name='_IS_ACTIVE')
    confirm_status = models.BooleanField(default=False, verbose_name='_CONFIRM_STATUS')
>>>>>>> upstream/dirty
    def __unicode__(self):
        return '%s' % (self.id)


class QuotedItem(models.Model):
<<<<<<< HEAD
    quote_order = models.ForeignKey(QuotedOrder)
    price = models.IntegerField(default = 0)
    qty = models.IntegerField()
    item = models.ForeignKey(Product)
=======
    quote_order = models.ForeignKey(QuotedOrder, verbose_name='_QUOTE_ORDER')
    price = models.IntegerField(default = 0, verbose_name='_PRICE')
    qty = models.IntegerField()
    item = models.ForeignKey(Product, verbose_name='_ITEM')
>>>>>>> upstream/dirty
    def save(self):
        if not self.id:
            self.price = self.item.price_per_unit * self.qty
        super(QuotedItem,self).save()

    def __unicode__(self):
        return '%s' % (self.item) + ' - ' '%s' % (self.quote_order)

 
class QuoteTaxesApplied(models.Model):
<<<<<<< HEAD
    quote_order = models.ForeignKey(QuotedOrder)
=======
    quote_order = models.ForeignKey(QuotedOrder, verbose_name='_QUOTE_ORDER')
>>>>>>> upstream/dirty
    surcharge = models.ForeignKey(Surcharge)
    tax = models.IntegerField()


class QuotedBill(models.Model):
    quote_order = models.ForeignKey(QuotedOrder)
    total_cost = models.IntegerField()
    total_tax = models.IntegerField()
    grand_total = models.IntegerField()
   




