from django.db import models
from django.urls import reverse

# Create your models here.

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

    def get_absolute_url(self):
        return reverse("list-l1groups")

    def __str__(self):

       return self.l1group

    class Meta:
        ordering = ['l1group']


class Account(models.Model):
    account = models.CharField(max_length=255, unique=True)
    active = models.BooleanField(verbose_name='Active', default=True)

    def get_absolute_url(self):
        return reverse("add-account")

    def __str__(self):
        return self.account

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

class Payee(models.Model):
    payee = models.CharField(max_length=255, unique=True)
    def_gcat = models.ForeignKey(GroupedCat, on_delete=models.PROTECT, null=True, blank=True)
    active = models.BooleanField(verbose_name='Active', default=True)


    def get_absolute_url(self):
        return reverse("add-payee")

    def __str__(self):
        t = str(self.payee)
        return t

    class Meta:
        ordering = ["payee"]
