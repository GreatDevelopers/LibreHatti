"""
models of catalog are..
"""
from django.db import models
from django.forms import ModelForm
import useraccounts
from django.contrib.auth.models import User

"""
This class defines the name of category and parent category of product 
"""
class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', blank=True, null=True)
    def __unicode__(self):
        return unicode(self.name)

"""
This class defines the name of product, category, price of eact item of 
that product and the organisation with which user deals
"""
class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category)
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
    def __unicode__(self):
        return self.name

"""
This class defines the details about user, its organisation, along with 
total discount and payment of job, and mode of payment
"""
class ModeOfPayment(models.Model):
    method = models.CharField(max_length=25)
    def __unicode__(self):
        return self.method

class PurchaseOrder(models.Model):
    buyer = models.ForeignKey(User)
    is_debit = models.BooleanField(default = False)
    delivery_address = models.ForeignKey('useraccounts.Address')
    organisation = models.ForeignKey('useraccounts.AdminOrganisations')
    date_time = models.DateTimeField(auto_now_add=True)
    total_discount = models.IntegerField()
    tds = models.IntegerField()
    mode_of_payment = models.ForeignKey(ModeOfPayment)
    is_canceled = models.BooleanField(default = False)
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


"""
This class defines the features, value of product
"""
class Catalog(models.Model):
    attribute = models.ForeignKey(Attributes)
    value = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    def __unicode__(self):
        return self.attribute.name;
"""
This class defines the type of taxes, value, validation of taxes 
mentioning the startdate and end date 
"""
class Surcharge(models.Model):
    tax_name = models.CharField(max_length=200)
    value = models.IntegerField()
    taxes_included = models.BooleanField(default = False)
    tax_effected_from = models.DateField()
    tax_valid_till = models.DateField()
    Remark = models.CharField(max_length=1000)
    def __unicode__(self):
         return self.tax_name


class Transport(models.Model):
    vehicle_id = models.CharField(max_length=20)
    job_id = models.IntegerField()
    kilometer = models.FloatField()
    rate = models.FloatField(default=10.0)  
    Date = models.DateField(blank=True)
    total = models.IntegerField()
    def __unicode__(self):
        return '%s' % (self.vehicle_id)
