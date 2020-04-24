# -*- coding: utf-8 -*-
from django.db import models
from librehatti.suspense.models import Staff, Vehicle


class TeamName(models.Model):
    """Model for team"""

    team_name = models.CharField(max_length=500)

    def __str__(self):
        return self.team_name


class StaffInTeam(models.Model):
    """Model for staff in team"""

    team_name = models.ForeignKey(TeamName, on_delete=models.CASCADE)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.staff) + " - " "%s" % (self.team_name)


class LetterData(models.Model):
    """Model for data required for letter generation"""

    name = models.CharField(max_length=500)
    street_address = models.CharField(max_length=500)
    district = models.CharField(max_length=500)
    pin = models.CharField(max_length=10, blank=True, null=True)
    province = models.CharField(max_length=500)
    contact_person = models.CharField(max_length=200)
    contact_number = models.IntegerField()
    letter_subject = models.CharField(max_length=500)
    letter_date = models.DateField(auto_now_add=True)
    team_name = models.ForeignKey(TeamName, on_delete=models.CASCADE)
    site = models.CharField(max_length=500)
    date = models.DateField()
    time = models.TimeField()
    vehicle = models.ForeignKey(Vehicle, default=1, on_delete=models.CASCADE)

    def __str__(self):
        return "%s" % (self.letter_subject) + " -- TEAM NAME: " "%s" % (
            self.team_name
        )
