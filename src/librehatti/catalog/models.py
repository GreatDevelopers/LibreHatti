from django.db import models
from django.forms import ModelForm
import useraccounts
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True)
    def __unicode__(self):
        return unicode(self.name)


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
    price_per_unit = models.IntegerField()
    organisation = models.ForeignKey('useraccounts.AdminOrganisations')
    def __unicode__(self):
        return self.name


class Attributes(models.Model):
    name = models.CharField(max_length=200)
    is_number = models.BooleanField(default = True)
    is_string = models.BooleanField(default = False)
    def __unicode__(self):
        return self.name

class ModeOfPayment(models.Model):
    method = models.CharField(max_length=25)
    def __unicode__(self):
        return self.method

class PurchaseOrder(models.Model):
    buyer_id = models.ForeignKey(User)
    is_debit = models.BooleanField(default = False)
    delivery_address = models.ForeignKey('useraccounts.Address')
    organisation = models.ForeignKey('useraccounts.AdminOrganisations')
    date_time = models.DateTimeField(auto_now_add=True)
    total_discount = models.IntegerField()
    tds = models.IntegerField()
    mode_of_payment = models.ForeignKey(ModeOfPayment)

    def __unicode__(self):
        return '%s' % (self.id)
               

class PurchasedItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder)
    price = models.IntegerField()
    qty = models.IntegerField()
    item = models.ForeignKey(Product)
    def save(self, *args, **kwargs):
        if not self.id:
            self.price = self.item.price_per_unit * self.qty	    
        super(PurchasedItem, self).save(*args, **kwargs) 

    def __unicode__(self):
        return '%s' % (self.item) + ' - ' '%s' % (self.purchase_order)


class Catalog(models.Model):
    attribute = models.ForeignKey(Attributes)
    value = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    def __unicode__(self):
        return self.attribute.name;

class Surcharge(models.Model):
    taxes = models.CharField(max_length=200)
    value = models.IntegerField()
    taxes_included = models.BooleanField(default = False)
    tax_effected_from = models.DateField()
    tax_valid_till = models.DateField()
    Remark = models.CharField(max_length=1000)
    def __unicode__(self):
         return self.taxes


