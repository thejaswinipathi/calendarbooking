from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class slots(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dateSlot = models.DateTimeField(null = False)
