from django.db import models

# Create your models here.
class Job(models.Model):
       employer = models.CharField(max_length=255, blank=True, null=True)
       job_title = models.CharField(max_length=255, blank=True, null=True)
       salary = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2, blank=True, null=True)
       bonus = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2, blank=True, null=True)
       state = models.CharField(max_length=2, blank=True, null=True)
       start_date = models.DateField(verbose_name='Date', blank=True, null=True)
       end_date = models.DateField(verbose_name='Date', blank=True, null=True)