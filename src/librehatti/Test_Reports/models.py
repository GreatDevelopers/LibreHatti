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

class Soil_building(models.Model):
    Session = models.ForeignKey(FinancialSession)
    Voucher = models.CharField(max_length=200)
    Date_of_Testing = models.DateField(verbose_name = _TEST_DATE)
    Type_of_str = models.CharField(max_length = 200, null=True, blank=True)    
    Latitude_N = models.CharField(max_length = 200, null=True, blank=True)
    Longitude_E = models.CharField(max_length = 200, null=True, blank=True)
    Presence_1 = models.CharField(max_length = 200, null=True, blank=True)
    Presence_2 = models.CharField(max_length = 200, null=True, blank=True)
    Submitted_1 = models.CharField(max_length = 200, null=True, blank=True)
    Submitted_2 = models.CharField(max_length = 200, null=True, blank=True)
    Submitted_3 = models.CharField(max_length = 200, null=True, blank=True)
    Site_Name = models.CharField(max_length = 200, null=True, blank=True)
    Bore_Hole = models.CharField(max_length = 200, null=True, blank=True)
    Water_Table = models.CharField(max_length = 200, null=True, blank=True)
    Wall_Dt = models.CharField(max_length = 200, null=True, blank=True)
    Wall_B = models.CharField(max_length = 200, null=True, blank=True)
    Col_Df = models.CharField(max_length = 200, null=True, blank=True)
    Col_L = models.CharField(max_length = 200, null=True, blank=True)
    Col_B = models.CharField(max_length = 200, null=True, blank=True)
    Gama_wall = models.CharField(max_length = 200, null=True, blank=True)
    Wall_C = models.CharField(max_length = 200, null=True, blank=True)
    Wall_Phay = models.CharField(max_length = 200, null=True, blank=True)
    Wall_Phay_Fe = models.CharField(max_length = 200, null=True, blank=True)
    Wall_Nc = models.CharField(max_length = 200, null=True, blank=True)
    Wall_Nq = models.CharField(max_length = 200, null=True, blank=True)
    Wall_Ny = models.CharField(max_length = 200, null=True, blank=True)
    Wall_Sc = models.CharField(max_length = 200, null=True, blank=True)
    Wall_Sq = models.CharField(max_length = 200, null=True, blank=True)
    Wall_Sy = models.CharField(max_length = 200, null=True, blank=True)
    Wall_dc = models.CharField(max_length = 200, null=True, blank=True)
    Wall_dq_dy = models.CharField(max_length = 200, null=True, blank=True)
    Wall_w = models.CharField(max_length = 200, null=True, blank=True)
    Wall_peq = models.CharField(max_length = 200, null=True, blank=True)
    Wall_Total = models.CharField(max_length = 200, null=True, blank=True)
    Wall_T_2 = models.CharField(max_length = 200, null=True, blank=True)
    Col_Sc = models.CharField(max_length = 200, null=True, blank=True)
    Col_Sq = models.CharField(max_length = 200, null=True, blank=True)
    Col_Sy = models.CharField(max_length = 200, null=True, blank=True)
    Col_dc = models.CharField(max_length = 200, null=True, blank=True)
    Col_dq_dy = models.CharField(max_length = 200, null=True, blank=True)
    Col_peq = models.CharField(max_length = 200, null=True, blank=True)
    Col_Total = models.CharField(max_length = 200, null=True, blank=True)
    Col_T_2 = models.CharField(max_length = 200, null=True, blank=True)
    Wall_N_V = models.CharField(max_length = 200, null=True, blank=True)
    Wall_S = models.CharField(max_length = 200, null=True, blank=True)
    Wall_Value = models.CharField(max_length = 200, null=True, blank=True)
    Wall_Net_V = models.CharField(max_length = 200, null=True, blank=True)
    Wall_G_V = models.CharField(max_length = 200, null=True, blank=True)
    Col_N_V = models.CharField(max_length = 200, null=True, blank=True)
    Col_Value = models.CharField(max_length = 200, null=True, blank=True)
    Col_Net_V = models.CharField(max_length = 200, null=True, blank=True)
    Col_G_V = models.CharField(max_length = 200, null=True, blank=True)

    def __unicode__(self):
        return '%s' % (self.Voucher) + ' - ' '%s' % (self.Date_of_Testing)

class Soil_building_des(models.Model):
    soil_building_report_id = models.ForeignKey(Soil_building)
    Dt = models.CharField(max_length = 200, null=True, blank=True)
    Ob_Pr = models.CharField(max_length = 200, null=True, blank=True)
    Corr_F = models.CharField(max_length = 200, null=True, blank=True)
    Ob_N_V  =   models.CharField(max_length = 200, null=True, blank=True)
    Corr_N_V = models.CharField(max_length = 200, null=True, blank=True)
