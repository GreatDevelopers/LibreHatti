from django.db import models

import useraccounts

from librehatti.catalog.models import Product

from librehatti.catalog.models import ModeOfPayment

from librehatti.catalog.models import Surcharge

from librehatti.bills.models import *

from django.contrib.auth.models import User

from librehatti.config import _REFERENCE_DATE

from librehatti.config import _CUBE_TEST

from librehatti.config import _TEST_DATE

from librehatti.voucher.models import FinancialSession

from django.core.urlresolvers import reverse


class Test_Reports(models.Model):
    Session = models.ForeignKey(FinancialSession)
    Voucher = models.CharField(max_length=200)
    Client = models.CharField(max_length=200)
    mix = models.BooleanField(default=False)
    Address = models.CharField(max_length=200)
    City = models.CharField(max_length=200)
    Subject = models.CharField(max_length=200)
    Refernce_no = models.CharField(max_length=200)
    Refernce_Date = models.DateField(verbose_name=_REFERENCE_DATE)
    Testing_Date = models.DateField(verbose_name=_TEST_DATE)


    def __unicode__(self):
	return unicode(self.Voucher)


class Test_Report_Descriptions(models.Model):
    report_id = models.ForeignKey(Test_Reports)
    Start_Date = models.DateField(verbose_name=_CUBE_TEST)
    Description = models.CharField(max_length=200)
    Strength = models.CharField(max_length=20)
    mix = models.CharField(max_length=200, null=True, blank=True)


    def __unicode__(self):
        return unicode(self.report_id)
