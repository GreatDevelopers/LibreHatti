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
    price = models.IntegerField()
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
    def __unicode__(self):
        return '%s' % (self.buyer_id) +' - ' '%s' % (self.date_time.strftime
               ('%b %d, %Y'))


class PurchasedItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder)
    price = models.IntegerField()
    qty = models.IntegerField()
    discount= models.IntegerField()
    item = models.ForeignKey(Product)
    def save(self):
        if not self.id:
            self.price = self.item.price * self.qty
        super(purchased_item,self).save()

    def __unicode__(self):
        return '%s' % (self.item) + ' - ' '%s' % (self.purchase_order)


class Catalog(models.Model):
    attribute = models.ForeignKey(Attributes)
    value = models.CharField(max_length=200)
    product = models.ForeignKey(Product)
    def __unicode__(self):
        return self.attribute.name;

