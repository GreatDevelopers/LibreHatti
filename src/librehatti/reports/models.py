from django.db import models

class SavedRegisters(models.Model):
    """
    This class saves the register generated.
    """
    title = models.CharField(max_length = 200)
    selected_fields = models.CharField(max_length = 1000)

    def __unicode__(self):
    	return self.title