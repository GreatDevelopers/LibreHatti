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
    price_per_unit = models.IntegerField()
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
    tax_name = models.CharField(max_length=200)
    value = models.FloatField()
    taxes_included = models.BooleanField(default = False)
    tax_effected_from = models.DateField(null = True)
    tax_valid_till = models.DateField(null = True)
    Remark = models.CharField(max_length=1000, null = True)
    def __unicode__(self):
         return self.tax_name


class PurchaseOrder(models.Model):
    buyer = models.ForeignKey(User)
    is_debit = models.BooleanField(default = False)
    reference = models.CharField(max_length=200)
    delivery_address = models.ForeignKey('useraccounts.Address')
    organisation = models.ForeignKey('useraccounts.AdminOrganisations')
    date_time = models.DateTimeField(auto_now_add=True)
    total_discount = models.IntegerField(default = 0)
    tds = models.IntegerField(default = 0)
    mode_of_payment = models.ForeignKey(ModeOfPayment)
    is_active = models.BooleanField(default = True)
    def save(self, *args, **kwargs):

        surchages = Surcharge.objects.filter(taxes_included=1)

        if surchages:
            super(PurchaseOrder, self).save(*args, **kwargs)
        else:
            raise ValidationError('No Active Taxes. Unable to add Order')
    def __unicode__(self):
        return '%s' % (self.id)


class PurchasedItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder)
    price = models.IntegerField()
    qty = models.IntegerField()
    item = models.ForeignKey(Product)
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
    purchase_order = models.ForeignKey(PurchaseOrder)
    surcharge = models.ForeignKey(Surcharge)
    tax = models.IntegerField()


class Vehicle(models.Model):
    vehicle_id = models.CharField(max_length=20)
    vehicle_no = models.CharField(max_length=20)
    vehicle_name = models.CharField(max_length=20)
    def __unicode__(self):
        return '%s' % (self.vehicle_id)


class Transport(models.Model):
    vehicle_id = models.ForeignKey(Vehicle)
    job_id = models.IntegerField()
    kilometer = models.FloatField()
    rate = models.FloatField(default=10.0)
    Date = models.DateField(blank=True)
    total = models.IntegerField()

    class Meta:
        verbose_name_plural = "Transport"

    def __unicode__(self):
        return '%s' % (self.vehicle_id)

"""
This class defines the grand total of the purchase order
"""

class Bill(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder)
    delivery_charges = models.IntegerField()
    total_cost = models.IntegerField()
    total_tax = models.IntegerField()
    grand_total = models.IntegerField()
    amount_received = models.IntegerField()

class HeaderOfBills(models.Model):
    header = HTMLField()
    def __unicode__(self):
        return '%s' % (self.id)

    class Meta:
        verbose_name_plural = "Header of bills"

