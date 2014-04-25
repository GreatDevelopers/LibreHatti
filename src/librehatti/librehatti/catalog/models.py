from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

"""
Models for cart module
"""

class organisation_type(models.Model):
    """docstring for organisation_type"""
    type_desc = models.CharField(max_length = 200)
    def __unicode__(self):
        return self.type_desc
        


class address(models.Model):
    """docstring for address"""
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)
    province = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    def __unicode__(self):
        return self.street_address + ", " + self.city

class user(models.Model):
    """

    """
    user = models.OneToOneField(User) 
    address = models.ForeignKey(address)
    email_address = models.EmailField(max_length = 70, blank = True, null = True)
    telephone = models.CharField(max_length = 500)
    date_joined  = models.DateTimeField(auto_now_add = True)
    fax = models.CharField(max_length = 100)
    avatar = models.CharField(max_length = 100, null=True, blank=True)
    tagline = models.CharField(max_length = 140)
    class Meta:
        abstract = True

class admin_organisations(user):
    """docstring for organisation"""
    title = models.CharField(max_length = 200)
    organisation_type = models.ForeignKey(organisation_type)
    def __unicode__(self):
        return self.title

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
    total = models.IntegerField()
    buyer_id = models.ForeignKey(User)
    is_debit = models.BooleanField()
    organisation = models.ForeignKey(admin_organisations)
    date_time = models.DateTimeField(auto_now_add=True)
    def __init__(self, arg):
        super(purchase_order, self).__init__()
        self.arg = arg

class purchased_item(models.Model):
    """docstring for purchased_item"""
    purchase_order = models.ForeignKey(purchase_order)
    price = models.IntegerField()
    item = models.ForeignKey(product)
    organisation = models.ForeignKey(admin_organisations)
    def __init__(self, arg):
        super(purchased_item, self).__init__()
        self.arg = arg


class catalog(models.Model):
    attribute = models.ForeignKey(attributes)
    value = models.CharField(max_length = 200)
    product = models.ForeignKey(product)
    organisation = models.ForeignKey(admin_organisations)
    def __unicode__(self):
        return self.attribute.name;


class customer(user):
    """docstring for customer"""
    first_name = models.CharField(max_length = 50)
    last_name = models.CharField(max_length = 50)
    title = models.CharField(max_length = 200, blank=True, null=True)
    is_org = models.BooleanField();
    org_type = models.ForeignKey(organisation_type)
    company = models.CharField(max_length = 200)
    def __init__(self, arg):
        super(customer, self).__init__()
        self.arg = arg
