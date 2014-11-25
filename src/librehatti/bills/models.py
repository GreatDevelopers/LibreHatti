from django.db import models
import useraccounts
from librehatti.catalog.models import Product
from librehatti.catalog.models import ModeOfPayment
from librehatti.catalog.models import Surcharge
from django.contrib.auth.models import User

from librehatti.config import _BUYER
from librehatti.config import _DELIVERY_ADDRESS
from librehatti.config import _IS_DEBIT
from librehatti.config import _PURCHASED_ITEMS
from librehatti.config import _QTY

from tinymce.models import HTMLField

class QuoteNote(models.Model):
    note = HTMLField()
    is_active = models.BooleanField(default = False)
    def save(self, *args, **kwargs):
        if self.is_active == True:
            if QuoteNote.objects.filter(is_active=1):
                raise ValidationError('Previous Active Note')
            else:
                super(QuoteNote, self).save(*args, **kwargs)
        else:
            super(QuoteNote, self).save(*args, **kwargs)
    def __unicode__(self):
        return '%s' % (self.id)

    class Meta:
        verbose_name_plural = "Quoted Order Note"

class QuotedOrder(models.Model):
    buyer = models.ForeignKey(User,verbose_name= _BUYER)
    is_debit = models.BooleanField(default = False, verbose_name = _IS_DEBIT)
    reference = models.CharField(max_length=200)
    delivery_address = models.CharField(max_length=500, blank=True, null=True,\
        verbose_name = _DELIVERY_ADDRESS)
    organisation = models.ForeignKey('useraccounts.AdminOrganisations')
    date_time = models.DateTimeField(auto_now_add=True)
    total_discount = models.IntegerField(default = 0)
    tds = models.IntegerField(default = 0)
    mode_of_payment = models.ForeignKey(ModeOfPayment)
    cheque_dd_number = models.CharField(max_length=50, blank=True)
    cheque_dd_date = models.DateField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default = True)
    def __unicode__(self):
        return '%s' % (self.id)


class QuotedItem(models.Model):
    quoted_order = models.ForeignKey(QuotedOrder)
    price = models.IntegerField()
    qty = models.IntegerField(verbose_name = _QTY)
    item = models.ForeignKey(Product)
    def save(self, *args, **kwargs):
        if self.quoted_order:
            self.price = self.item.price_per_unit * self.qty
            super(QuotedItem,self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % (self.item) + ' - ' '%s' % (self.quote_order)

 
class QuotedTaxesApplied(models.Model):
    quoted_order = models.ForeignKey(QuotedOrder)
    surcharge = models.ForeignKey(Surcharge)
    tax = models.IntegerField()
    def __unicode__(self):
        return "%s" % (self.surcharge)


class QuotedBill(models.Model):
    quoted_order = models.ForeignKey(QuotedOrder)
    delivery_charges = models.IntegerField()
    total_cost = models.IntegerField()
    total_tax = models.IntegerField()
    grand_total = models.IntegerField()
    amount_received = models.IntegerField()
   




