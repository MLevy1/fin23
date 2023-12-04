from django.db import models

# Create your models here.
class Location(models.Model):
       location_name = models.CharField(max_length=255, unique=True, blank=True, null=True)
       address = models.CharField(max_length=255, unique=True, blank=True, null=True)
       city = models.CharField(max_length=255, blank=True, null=True)
       start_date = models.DateField(verbose_name='Date', blank=True, null=True)
       end_date = models.DateField(verbose_name='Date', null=True, blank=True)