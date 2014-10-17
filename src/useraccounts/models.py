"""
Models for the useraccounts are..
"""
from django.db import models
from django.contrib.auth.models import User
import conf

"""
describes the type of organisation where the user deals
"""
class OrganisationType(models.Model):    
    type_desc = models.CharField(max_length=200)
    def __unicode__(self):
        return self.type_desc

"""
describes the address details of the admin organisation 
"""
class Address(models.Model):
    street_address = models.CharField(max_length=100, verbose_name=_STREET_ADDRESS)
    city = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)
    province = models.CharField(max_length=100, verbose_name=_PROVINCE)
    nationality = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Addresses"

    def __unicode__(self):
        return self.street_address + ',' + self.city

"""
describes the details of the user's organisation 
"""
class HattiUser(models.Model):   
    user = models.OneToOneField(User, verbose_name=_USER) 
    address = models.ForeignKey(Address)
    telephone = models.CharField(max_length=500, verbose_name=_TELEPHONE)
    date_joined  = models.DateTimeField(auto_now_add=True, verbose_name=_DATE_JOINED)
    fax = models.CharField(max_length=100)
    pan_no = models.CharField(max_length=100)
    stc_no = models.CharField(max_length=100)
    avatar = models.CharField(max_length=100, null=True, blank=True)
    tagline = models.CharField(max_length=140)
    class Meta:
        abstract=True

"""
This class inherits the details of HattiUser specifying the title of 
organisation and its type   
"""
class AdminOrganisations(HattiUser):
    title = models.CharField(max_length=200)
    organisation_type = models.ForeignKey(OrganisationType, verbose_name=_ORGANISATION_TYPE)

    class Meta:
        verbose_name_plural = "Admin Organisations"

    def __unicode__(self):
        return self.title

"""
This class inherits the details of HattiUser whether customer is
organisation type or individual thus customer will confirm the Is org
checkbox and then specifying the type of oganisation and its company
name 
"""
class Customer(HattiUser):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name=_TITLE)
    is_org = models.BooleanField(default = False);
    org_type = models.ForeignKey(OrganisationType)
    company = models.CharField(max_length=200, verbose_name=_COMPANY)
    def __unicode__(self):
	return unicode(self.user)
