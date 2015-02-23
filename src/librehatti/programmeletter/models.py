from django.db import models
import useraccounts

from django.contrib.auth.models import User
from librehatti.config import _BUYER

from librehatti.suspense.models import Staff
from librehatti.suspense.models import Vehicle


class TeamName(models.Model):
    """Model for team"""
    team_name = models.CharField(max_length=500)
    def __unicode__(self):
        return self.team_name


class StaffInTeam(models.Model):
    """Model for staff in team"""
    team_name = models.ForeignKey(TeamName)
    staff = models.ForeignKey(Staff)
    def __unicode__(self):
        return '%s' % (self.staff) + ' - ' '%s' % (self.team_name)


class LetterData(models.Model):
    """Model for data required for letter generation"""
    buyer = models.ForeignKey(User,verbose_name= _BUYER)
    contact_person = models.CharField(max_length=200)
    contact_number = models.IntegerField()
    letter_subject = models.CharField(max_length=500)
    letter_date = models.DateField(auto_now_add=True)
    team_name = models.ForeignKey(TeamName)
    site = models.CharField(max_length=500)
    date = models.DateField()
    time = models.TimeField()
    vehicle = models.ForeignKey(Vehicle, default=1)
    def __unicode__(self):
        return '%s' % (self.letter_subject) + ' -- TEAM NAME: ' '%s' % (self.team_name)
