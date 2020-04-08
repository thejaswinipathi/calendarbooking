from django.db import models
from django.conf import settings
# Create your models here.

class slots(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null = False)
    dateFromSlot = models.DateTimeField(null = False)
    class Meta:
        unique_together = ('dateFromSlot', 'user')