from django.db import models
from simple_history.models import HistoricalRecords

# Create your models here.

class Payee(models.Model):
    payee = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(verbose_name='Active', default=True)
    history = HistoricalRecords()
    
    def __str__(self):

        t = str(self.payee)  +  "[ " + str(self.id) + " ]"

        return t
    
    class Meta:
        ordering = ["payee"]

class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.category
    
    class Meta:
        ordering = ["category"]
        verbose_name_plural = "Categories"


class Account(models.Model):
    account = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(verbose_name='Active', default=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.account
    
    class Meta:
        ordering = ["account"]


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

		
class Trans(models.Model):
	tid = models.IntegerField(null=True)
	tdate = models.DateField(verbose_name='Date')
	amount = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2)
	account =  models.ForeignKey(Account, on_delete=models.CASCADE)
	payee = models.ForeignKey(Payee, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	match = models.CharField(max_length=255, null=True, blank=True)
	oldCat = models.CharField(max_length=255, null=True, blank=True)
	oldPayee = models.CharField(max_length=255, null=True, blank=True)
	note = models.CharField(max_length=255, null=True, blank=True)
	history = HistoricalRecords()
	
           
	def __str__(self):

		t = str(self.tdate) + " " + str(self.payee) + ": " + str(self.amount) +  "[ " + str(self.tid) + " ]"

		return str(t)

	class Meta:
		ordering = ["tdate", "amount"]