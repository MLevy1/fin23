from django.db import models
from simple_history.models import HistoricalRecords
from django_pandas.managers import DataFrameManager
from django.urls import reverse
from tagging.fields import TagField

# Create your models here.

class Payee(models.Model):
    payee = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(verbose_name='Active', default=True)
    tags = TagField()

    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse("add_payee")
        
    def __str__(self):

        t = str(self.payee)  +  "[ " + str(self.id) + " ]"

        return t
    
    class Meta:
        ordering = ["payee"]

class L1Group(models.Model):
    l1group = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(verbose_name='Active', default=True)

    def get_absolute_url(self):
        return reverse("list-l1group")
    
    def __str__(self):
       
       return self.l1group

    class Meta:
        ordering = ['l1group']

class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(verbose_name='Active', default=True)

    def get_absolute_url(self):
        return reverse("add_cat")

    def __str__(self):
        return self.category
    
    class Meta:
        ordering = ["category"]
        verbose_name_plural = "Categories"

class Account(models.Model):
    account = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(verbose_name='Active', default=True)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse("add_account")

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

class GroupedCat(models.Model):
	l1group =  models.ForeignKey(L1Group, on_delete=models.CASCADE, blank=True, null=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
	
	def __str__(self):

		t = str(self.l1group) + " > " + str(self.category)

		return str(t)
     
	def get_absolute_url(self):
		return reverse("list-gc")
		
	class Meta:
        	ordering = ["l1group__l1group", "category"]

class Trans(models.Model):
	tid = models.IntegerField(null=True)
	tdate = models.DateField(verbose_name='Date')
	amount = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2)
	account =  models.ForeignKey(Account, on_delete=models.CASCADE)
	payee = models.ForeignKey(Payee, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	groupedcat = models.ForeignKey(GroupedCat, on_delete=models.CASCADE, null=True, blank=True)
	match = models.CharField(max_length=255, null=True, blank=True)
	oldCat = models.CharField(max_length=255, null=True, blank=True)
	oldPayee = models.CharField(max_length=255, null=True, blank=True)
	note = models.CharField(max_length=255, null=True, blank=True)
	history = HistoricalRecords()
	tag = TagField()

	objects = DataFrameManager()

	def __str__(self):

		t = str(self.tdate) + " " + str(self.payee) + ": " + str(self.amount) +  "[ " + str(self.tid) + " ]"

		return str(t)

	class Meta:
		ordering = ["tdate", "amount"]


class Location(models.Model):
       location_name = models.CharField(max_length=255, unique=True, blank=True, null=True)
       address = models.CharField(max_length=255, unique=True, blank=True, null=True)
       city = models.CharField(max_length=255, blank=True, null=True)
       start_date = models.DateField(verbose_name='Date', blank=True, null=True)
       end_date = models.DateField(verbose_name='Date', null=True, blank=True)


class Job(models.Model):
       employer = models.CharField(max_length=255, blank=True, null=True)
       job_title = models.CharField(max_length=255, blank=True, null=True)
       salary = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2, blank=True, null=True)
       bonus = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2, blank=True, null=True)
       state = models.CharField(max_length=2, blank=True, null=True)
       start_date = models.DateField(verbose_name='Date', blank=True, null=True)
       end_date = models.DateField(verbose_name='Date', blank=True, null=True)

class BudgetItem(models.Model):

    X = "Once"
    A = "Annual"
    S = "Semiannual"
    Q = "Quarterly"
    M = "Monthly"
    B = "Biweekly"
    W = "Weekly"
    D = "Daily"
    E = "Weekends"
    O = "Officedays"
    H = "Homeworkdays"
    V = "Vacationdays"

    FREQUENCY_CHOICES = [(X, "Once"), (A, "Annual"), (S, "Semiannual"), (Q, "Quarterly"), (M, "Monthly"), (B, "Biweekly"), (W, "Weekly"), (D, "Daily"), (E, "Weekends"), (O, "Officedays"), (H, "Homeworkdays"), (V, "Vacationdays")]

    itemName = models.CharField(verbose_name='Budget Item', max_length=100)
    itemFreq = models.CharField(verbose_name='Frequency', max_length=20, choices=FREQUENCY_CHOICES, default=M)
    itemAmt = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2)
    itemCat = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    
    def annualAmt(self):
        if self.itemFreq == 'once':
            return self.itemAmt
        elif self.itemFreq == 'Annual':
            return self.itemAmt
        elif self.itemFreq == 'Semiannual':
            return self.itemAmt * 2
        elif self.itemFreq == 'Quarterly':
            return self.itemAmt * 4
        elif self.itemFreq == 'Monthly':
            return self.itemAmt * 12
        elif self.itemFreq == 'Biweekly':
            return self.itemAmt * 26
        elif self.itemFreq == 'Weekly':
            return self.itemAmt * 52
        elif self.itemFreq == 'Daily':
            return self.itemAmt * 365
        elif self.itemFreq == 'Weekends':
            return self.itemAmt * 104  # 2 days per weekend and 52 weekends
        elif self.itemFreq == 'Officedays':
            return self.itemAmt * 144  # 3 days a week and 48 working weeks
        elif self.itemFreq == 'Homeworkdays':
            return self.itemAmt * 96  # 2 days a week and 48 working weeks
        elif self.itemFreq == 'Vacationdays':
            return self.itemAmt * 33  # 4 weeks & 13 holidays

    def __str__(self):

        t = str(self.id) + " " + str(self.itemName)

        return str(t)

