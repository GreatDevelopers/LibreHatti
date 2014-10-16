"""
models of catalog are..
"""
from django.db import models
from django.forms import ModelForm
import useraccounts
from django.contrib.auth.models import User
from django.http import HttpResponse
from mptt.models import MPTTModel, TreeForeignKey
import mptt.fields
from django.core.exceptions import ValidationError
import datetime

from tinymce.models import HTMLField

"""
This class defines the name of category and parent category of product
"""
class mCategory(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return unicode(self.name)

class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', null=True, blank=True, related_name="children")

    class MPTTMeta:
        order_insertion_by = ['name']

    def __unicode__(self):
        return '%s' % self.name

"""
This class defines the name of product, category, price of eact item of
that product and the organisation with which user deals
"""
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = mptt.fields.TreeForeignKey(Category, related_name="products")
    price_per_unit = models.IntegerField(verbose_name='_PRICE_PER_UNIT')
    organisation = models.ForeignKey('useraccounts.AdminOrganisations')
    def __unicode__(self):
        return self.name

"""
This class defines the features of product
"""
class Attributes(models.Model):
    name = models.CharField(max_length=200)
    is_number = models.BooleanField(default = True)
    is_string = models.BooleanField(default = False)

    class Meta:
        verbose_name_plural = "Attributes"

    def __unicode__(self):
        return self.name

"""
This class defines the details about user, its organisation, along with
total discount and payment of job, and mode of payment
"""
class ModeOfPayment(models.Model):
    method = models.CharField(max_length=25)

    class Meta:
        verbose_name_plural = "Modes of payment"

    def __unicode__(self):
        return self.method


"""
This class defines the type of taxes, value, validation of taxes
mentioning the startdate and end date
"""
class Surcharge(models.Model):
    tax_name = models.CharField(max_length=200, verbose_name='_TAX_NAME')
    value = models.FloatField()
    taxes_included = models.BooleanField(default = False)
    tax_effected_from = models.DateField(null = True, verbose_name='_TAX_EFFECTED_FROM')
    tax_valid_till = models.DateField(null = True, verbose_name='_TAX_VALID_TILL')
    Remark = models.CharField(max_length=1000, null = True)
    def __unicode__(self):
         return self.tax_name


class PurchaseOrder(models.Model):
    buyer = models.ForeignKey(User, verbose_name='_BUYER')
    is_debit = models.BooleanField(default = False)
    reference = models.CharField(max_length=200)
    delivery_address = models.CharField(max_length=500, blank=True, null=True, verbose_name='_DELIVERY_ADDRESS')
    organisation = models.ForeignKey('useraccounts.AdminOrganisations', verbose_name='_ORGANISATION')
    date_time = models.DateTimeField(auto_now_add=True)
    total_discount = models.IntegerField(default = 0)
    tds = models.IntegerField(default = 0)
    mode_of_payment = models.ForeignKey(ModeOfPayment, verbose_name='_MODE_OF_PAYMENT')
    cheque_dd_number = models.CharField(max_length=50, blank=True)
    cheque_dd_date = models.DateField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default = True)
    def save(self, *args, **kwargs):

        surchages = Surcharge.objects.filter(taxes_included=1)

        if surchages:
            pass
        else:
            raise ValidationError('No Active Taxes. Unable to add Order')
        from librehatti.voucher.models import FinancialSession
        now = datetime.datetime.now()
        financialsession = FinancialSession.objects.\
        values('id','session_start_date','session_end_date')
        for value in financialsession:
            start_date = value['session_start_date']
            end_date = value['session_end_date']
            if start_date <= now.date() <= end_date:
                session_id = value['id']
        try:
            session_id
            super(PurchaseOrder, self).save(*args, **kwargs)
        except:
            raise ValidationError('No Current Financial Session')
    def __unicode__(self):
        return '%s' % (self.id)


class PurchasedItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, verbose_name='_PURCHASE_ORDER')
    price = models.IntegerField(verbose_name='_PRICE')
    qty = models.IntegerField()
    item = models.ForeignKey(Product, verbose_name='_ITEM')
    def save(self, *args, **kwargs):
        try:
            if self.purchase_order:
                self.price = self.item.price_per_unit * self.qty
                super(PurchasedItem, self).save(*args, **kwargs)
        except:
            raise ValidationError('No Active Taxes. Unable to add Items')

    def __unicode__(self):
        return '%s' % (self.item) + ' - ' '%s' % (self.purchase_order)


"""
This class defines the features, value of product
"""
class Catalog(models.Model):
    attribute = models.ForeignKey(Attributes)
    value = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    def __unicode__(self):
        return self.attribute.name

"""
This class defines the taxes applied on the purchase order
"""
class TaxesApplied(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, verbose_name='_PURCHASE_ORDER')
    surcharge = models.ForeignKey(Surcharge)
    tax = models.IntegerField()



"""
This class defines the grand total of the purchase order
"""

class Bill(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, verbose_name='_PURCHASE_ORDER')
    delivery_charges = models.IntegerField(verbose_order='_DELIVERY_CHARGES')
    total_cost = models.IntegerField()
    total_tax = models.IntegerField()
    grand_total = models.IntegerField()
    amount_received = models.IntegerField()

class HeaderFooter(models.Model):
    header = HTMLField()
    footer = HTMLField()
    is_active = models.BooleanField(default = False)
    def save(self, *args, **kwargs):
        if self.is_active == True:
            if HeaderFooter.objects.filter(is_active=1):
                raise ValidationError('Previous Active Header and Footer')
            else:
                super(HeaderFooter, self).save(*args, **kwargs)
        else:
            super(HeaderFooter, self).save(*args, **kwargs)
    def __unicode__(self):
        return '%s' % (self.id)

    class Meta:
        verbose_name_plural = "Header and Footer"
