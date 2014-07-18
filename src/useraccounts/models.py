"""
Models for the catalog is described in this file
"""
from django.db import models
from django.contrib.auth.models import User

"""
Organisation name or type 
"""
class OrganisationType(models.Model):    
    type_desc = models.CharField(max_length=200)
    def __unicode__(self):
        return self.type_desc

"""
Organisation details 
"""
class Address(models.Model):
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)
    province = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    def __unicode__(self):
        return self.street_address + ',' + self.city

"""
User details 
"""
class HattiUser(models.Model):   
    user = models.OneToOneField(User) 
    address = models.ForeignKey(Address)
    telephone = models.CharField(max_length=500)
    date_joined  = models.DateTimeField(auto_now_add=True)
    fax = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100, null=True, blank=True)
    tagline = models.CharField(max_length=140)
    class Meta:
        abstract=True

"""
describes title of organisation and its type 
"""
class AdminOrganisations(HattiUser):
    title = models.CharField(max_length=200)
    organisation_type = models.ForeignKey(OrganisationType)
    def __unicode__(self):
        return self.title

"""
describes the name of company or organisation if buyer owns it
or buyer is not individual 
"""
class Customer(HattiUser):
    title = models.CharField(max_length=200, blank=True, null=True)
    is_org = models.BooleanField();
    org_type = models.ForeignKey(OrganisationType)
    company = models.CharField(max_length=200)
    def __unicode__(self):
	return unicode(self.user)
