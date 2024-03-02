from django.db import models

from fin.models import (
	Payee,
	Account,
)

class Csv(models.Model):
    file_name = models.FileField(upload_to='csvs')
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.id}"

class Imported_Payee(models.Model):
    imported_payee = models.CharField(max_length=255, unique=True)
    payee =  models.ForeignKey(Payee, on_delete=models.PROTECT, blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.imported_payee

class Staged_Transaction(models.Model):
    uploaded = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.PROTECT, blank=True, null=True)
    tdate = models.DateField(verbose_name='Date', null=True, blank=True)
    amount = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2, null=True, blank=True)
    imported_payee = models.ForeignKey(Imported_Payee, on_delete=models.PROTECT, blank=True, null=True)
    imported = models.BooleanField(default=False)

    ordering=['tdate']

    def __str__(self):
        return str(self.tdate) + " > " + str(self.imported_payee) + " > " + str(self.amount)