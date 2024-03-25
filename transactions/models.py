from django.db import models

from django.urls import reverse

from fin.models import (
	Account,
	Payee,
	GroupedCat
)

# Create your models here.
class Transaction(models.Model):
	tid = models.IntegerField(null=True)
	tdate = models.DateField(verbose_name='Date', null=True, blank=True)
	account = models.ForeignKey(Account, on_delete=models.PROTECT, null=True, blank=True)
	payee = models.ForeignKey(Payee, on_delete=models.PROTECT, null=True, blank=True)
	match = models.CharField(max_length=255, null=True, blank=True)
	note = models.CharField(max_length=255, null=True, blank=True)
	oldCat = models.CharField(max_length=255, null=True, blank=True)
	oldPayee = models.CharField(max_length=255, null=True, blank=True)

    #T14
	def get_absolute_url(self):
		return reverse("transactions:detail", kwargs={"id": self.id})

    #T4
	def get_edit_url(self):
		return reverse("transactions:update", kwargs={"id": self.id })

    #T5
	def get_delete_url(self):
		return reverse("transactions:delete", kwargs={"id": self.id})

	def get_transaction_total(self):
		tsum = 0
		for t in self.subtransaction_set.all():
			tsum += t.amount
		return tsum

	def get_subtrans_children(self):
		return self.subtransaction_set.all()

	def __str__(self):
		t = str(self.tdate) + " " + str(self.payee) + "[ " + str(self.tid) + " ]"
		return str(t)

	class Meta:
		ordering = ["tdate"]


class SubTransaction(models.Model):
	trans = models.ForeignKey(Transaction, on_delete=models.PROTECT, null=True, blank=True)
	amount = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2, null=True, blank=True)
	groupedcat = models.ForeignKey(GroupedCat, on_delete=models.PROTECT, null=True, blank=True)
	note = models.CharField(max_length=255, null=True, blank=True)

    #T14
	def get_absolute_url(self):
		return self.trans.get_absolute_url()

    #T7
	def get_delete_url(self):
		return reverse("transactions:subtran-delete", kwargs = {"parent_id": self.trans.id, "id": self.id})

    #T6
	def get_hx_edit_url(self):
		kwargs = {
			"parent_id": self.trans.id,
			"id": self.id
		}
		return reverse("transactions:hx-subtran-update", kwargs=kwargs)

	def __str__(self):
	    t = self.trans.tdate
	    c = self.groupedcat
	    a = self.amount
	    n = str(t)+' '+str(c)+' '+str(a)
	    return n


	class Meta:
		ordering = ["-amount"]
