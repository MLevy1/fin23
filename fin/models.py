from django.db import models
from django.db.models.signals import pre_save, post_save
from simple_history.models import HistoricalRecords
from django_pandas.managers import DataFrameManager
from django.urls import reverse
from tagging.fields import TagField

from .utils import slugify_instance_payee

# Create your models here.

class Payee(models.Model):
    payee = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(verbose_name='Active', default=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    tags = TagField()

    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse("add-payee")
 
    def __str__(self):

        t = str(self.payee)

        return t
    
    class Meta:
        ordering = ["payee"]

def payee_pre_save(sender, instance, *args, **kwargs):
    print('pre_save')
    if instance.slug is None:
        slugify_instance_payee(instance, save=False)

pre_save.connect(payee_pre_save, sender=Payee)

def payee_post_save(sender, instance, created, *args, **kwargs):
    print('post_save')
    if created:
        slugify_instance_payee(instance, save=True)

post_save.connect(payee_post_save, sender=Payee)

class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(verbose_name='Active', default=True)

    def get_absolute_url(self):
        return reverse("add-category")

    def __str__(self):
        return self.category
    
    class Meta:
        ordering = ["category"]
        verbose_name_plural = "Categories"

class L1Group(models.Model):
    l1group = models.CharField(max_length=255, unique=True)

    active = models.BooleanField(verbose_name='Active', default=True)

    aligned_category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("list-l1groups")
    
    def __str__(self):
       
       return self.l1group

    class Meta:
        ordering = ['l1group']


class Account(models.Model):
    account = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(verbose_name='Active', default=True)
    history = HistoricalRecords()

    def get_absolute_url(self):
        return reverse("add-account")

    def __str__(self):
        return self.account
    
    class Meta:
        ordering = ["account"]

class GroupedCat(models.Model):
	l1group =  models.ForeignKey(L1Group, on_delete=models.PROTECT, blank=True, null=True)
	category = models.ForeignKey(Category, on_delete=models.PROTECT, blank=True, null=True)
	
	def __str__(self):

		t = str(self.l1group) + " > " + str(self.category)

		return str(t)
     
	def get_absolute_url(self):
		return reverse("add-gc")
		
	class Meta:
        	ordering = ["l1group__l1group", "category"]

class Trans(models.Model):
	tid = models.IntegerField(null=True)
	tdate = models.DateField(verbose_name='Date')
	amount = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2)
	account =  models.ForeignKey(Account, on_delete=models.PROTECT)
	payee = models.ForeignKey(Payee, on_delete=models.PROTECT)
	category = models.ForeignKey(Category, on_delete=models.PROTECT)
	groupedcat = models.ForeignKey(GroupedCat, on_delete=models.PROTECT, null=True, blank=True)
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
		ordering = ["tdate", "-amount"]
		#ordering = ["category"]