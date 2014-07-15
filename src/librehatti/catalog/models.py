from django.db import models
from django.forms import ModelForm
import useraccounts
from django.contrib.auth.models import User
from librehatti.suspense.models import SuspenseOrder
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
    is_number = models.BooleanField()
    is_string = models.BooleanField()
    def __unicode__(self):
        return self.name


class PurchaseOrder(models.Model):
    buyer_id = models.ForeignKey(User)
    is_debit = models.BooleanField()
    delivery_address = models.ForeignKey('useraccounts.Address')
    organisation = models.ForeignKey('useraccounts.AdminOrganisations')
    date_time = models.DateTimeField(auto_now_add=True)
    total_discount = models.IntegerField()
    tds = models.IntegerField()
    is_suspense = models.BooleanField(default=False)
    choices = (('cash', 'Cash'), ('demand_draft', 'Demand Draft'), ('cheque', 'Cheque'))
    mode_of_payment = models.CharField(max_length=25, default='cash', choices=choices)
    def __unicode__(self):
        return '%s' % (self.buyer_id) +' - ' '%s' % (self.date_time.strftime
               ('%b %d, %Y'))

    def save(self, *args, **kwargs):
	if self.mode_of_payment=='cheque' or self.mode_of_payment=='demand_draft':
			self.is_suspense=True
	super(PurchaseOrder, self).save(*args, **kwargs) 

    

class PurchasedItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder)
    price = models.IntegerField()
    qty = models.IntegerField()
    discount= models.IntegerField()
    item = models.ForeignKey(Product)
    def save(self, *args, **kwargs):
	if not self.id:
            self.price = self.item.price * self.qty
	if self.item.category.parent.name=='Field Work':
	    a=self.purchase_order.id
	    b=PurchaseOrder.objects.filter(id=a).update(is_suspense=True)
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
    taxes_included = models.BooleanField()
    tax_effected_from = models.DateField()
    tax_valid_till = models.DateField()
    Remark = models.CharField(max_length=1000)
    def __unicode__(self):
         return self.taxes


