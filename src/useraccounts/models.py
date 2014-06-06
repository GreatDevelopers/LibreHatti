from django.db import models
from django.contrib.auth.models import User


class organisation_type(models.Model):    
    type_desc = models.CharField(max_length=200)
    def __unicode__(self):
        return self.type_desc


class address(models.Model):
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)
    province = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    def __unicode__(self):
        return self.street_address + ',' + self.city


class user(models.Model):   
    user = models.OneToOneField(User) 
    address = models.ForeignKey(address)
    telephone = models.CharField(max_length=500)
    date_joined  = models.DateTimeField(auto_now_add=True)
    fax = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100, null=True, blank=True)
    tagline = models.CharField(max_length=140)
    class Meta:
        abstract=True


class admin_organisations(user):
    title = models.CharField(max_length=200)
    organisation_type = models.ForeignKey(organisation_type)
    def __unicode__(self):
        return self.title


class customer(user):
    title = models.CharField(max_length=200, blank=True, null=True)
    is_org = models.BooleanField();
    org_type = models.ForeignKey(organisation_type)
    company = models.CharField(max_length=200)
    def __unicode__(self, arg):
	return unicode(self.user)
