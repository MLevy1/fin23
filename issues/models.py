from django.db import models

# Create your models here.
class Issue(models.Model):
    HIGH = "H"
    MEDIUM = "M"
    LOW = "L"

    PRIORITY_CHOICES = [(HIGH, "High"), (MEDIUM, "Medium"), (LOW, "Low")]

    opendate = models.DateTimeField(verbose_name='Open Date', auto_now_add=True)
    issuename = models.CharField(verbose_name='Issue Name', max_length=100)
    issuedesc = models.TextField(verbose_name='Isssue Description')
    priority = models.CharField(verbose_name='Priority Level', max_length=20, choices=PRIORITY_CHOICES, default=MEDIUM)
    issueopen = models.BooleanField(verbose_name='Issue Open', default=True)
    closedate = models.DateTimeField(verbose_name='Closed Date', blank=True, null=True)
    
    def __str__(self):

        t = str(self.id) + " " + str(self.issuename)

        return str(t)