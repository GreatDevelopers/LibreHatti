from django.db import models
from django.forms import ModelForm
from authentication.models import *

"""
Models for cart module
"""

class category(models.Model):
    name = models.CharField(max_length = 100)
    parent = models.ForeignKey('self',blank = True, null = True)
    def __unicode__(self):
        return unicode(self.name)

class product(models.Model):
    name = models.CharField(max_length = 100)
    category = models.ForeignKey(category)
    price = models.IntegerField()
    organisation = models.ForeignKey(admin_organisations)
    def __unicode__(self):
        return self.name

class attributes(models.Model):
    name = models.CharField(max_length=200)
    is_number = models.BooleanField()
    is_string = models.BooleanField()
    def __unicode__(self):
	   return self.name

class purchase_order(models.Model):
    """docstring for purchase_order"""
    buyer_id = models.ForeignKey(User)
    is_debit = models.BooleanField()
    organisation = models.ForeignKey(admin_organisations)
    date_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
	return '%s' % (self.buyer_id) +' - ' '%s' % (self.date_time.strftime('%b %d, %Y'))

class purchased_item(models.Model):
    """docstring for purchased_item"""
    purchase_order = models.ForeignKey(purchase_order)
    price = models.IntegerField()
    qty = models.IntegerField()
    discount= models.IntegerField()
    item = models.ForeignKey(product)
    def save(self):
	if not self.id:
		self.price = self.item.price * self.qty
	super(purchased_item,self).save()

    def __unicode__(self):
        return '%s' % (self.item) + ' - ' '%s' % (self.purchase_order)

class catalog(models.Model):
    attribute = models.ForeignKey(attributes)
    value = models.CharField(max_length = 200)
    product = models.ForeignKey(product)
    def __unicode__(self):
        return self.attribute.name;


