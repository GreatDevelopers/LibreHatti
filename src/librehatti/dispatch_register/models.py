"""
models of dispatch_register are..
"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class RemarksChoice(models.Model):
    """
    This class defines the remarks and parent category of DispatchEntry.
    """
    remark_name=models.CharField(max_length=200)

    def __str__(self):
        """
        This function will return the remark_name field of the associated
        object.
        """
        return self.remark_name

class SubjectsChoice(models.Model):
    """
    This class defines the subjects and parent category of DispatchEntry.
    """
    subject_name=models.CharField(max_length=200)

    def __str__(self):
        """
        This function will return the subject_name field of the associated
        object.
        """
        return self.subject_name

class DispatchEntry(models.Model):
    """
    This class defines the dispatch entry.
    """
    dispatch_no = models.AutoField(primary_key=True)
    date = models.DateTimeField(default=timezone.now)
    name_of_Dept_or_Client = models.ForeignKey(User)
    agency = models.CharField(max_length=200, blank=True)
    subjects = models.ManyToManyField(SubjectsChoice)
    remarks = models.ManyToManyField(RemarksChoice)
