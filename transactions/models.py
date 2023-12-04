from django.db import models

from django_pandas.managers import DataFrameManager

from fin.models import (
	Account,
	Payee,
	Category,
	GroupedCat
)

# Create your models here.
class Transaction(models.Model):
	tid = models.IntegerField(null=True)
	tdate = models.DateField(verbose_name='Date', null=True, blank=True)
	amount = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2, null=True, blank=True)
	account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, blank=True)
	payee = models.ForeignKey(Payee, on_delete=models.PROTECT, null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
	groupedcat = models.ForeignKey(GroupedCat, on_delete=models.PROTECT, null=True, blank=True)
	match = models.CharField(max_length=255, null=True, blank=True)
	note = models.CharField(max_length=255, null=True, blank=True)
	oldCat = models.CharField(max_length=255, null=True, blank=True)
	oldPayee = models.CharField(max_length=255, null=True, blank=True)

	objects = DataFrameManager()

	def __str__(self):

		t = str(self.tdate) + " " + str(self.payee) + ": " + str(self.amount) +  "[ " + str(self.tid) + " ]"

		return str(t)

	class Meta:
		ordering = ["tdate", "-amount"]
		#ordering = ["category"]


class SubTransaction(models.Model):
	trans = models.ForeignKey(Transaction, on_delete=models.PROTECT, null=True, blank=True)
	amount = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2, null=True, blank=True)
	category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
	groupedcat = models.ForeignKey(GroupedCat, on_delete=models.PROTECT, null=True, blank=True)
	note = models.CharField(max_length=255, null=True, blank=True)

	class Meta:
		ordering = ["-amount"]