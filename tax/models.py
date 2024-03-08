from django.db import models

from django.urls import reverse

from fin.models import (
    Payee,
)

# Create your models here.
class Tax_Return(models.Model):
    payee = models.ForeignKey(Payee, on_delete=models.PROTECT, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("tax:tax-return-detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("tax:tax-return-update", kwargs={"id": self.id })

    def get_delete_url(self):
        return reverse("tax:tax-return-delete", kwargs={"id": self.id})

    def get_list_url(self):
        return reverse("tax:tax-return-list")

    def get_children(self):
        return self.tax_return_form_set.all()

    def __str__(self):
        return str(self.year) + ": " + str(self.payee.payee)

class Tax_Return_Form(models.Model):

    tax_return = models.ForeignKey(Tax_Return, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    desc = models.CharField(max_length=255, null=True, blank=True)
    outbound = models.BooleanField(null=True, blank=True, default=True)

class Tax_Return_Form_Line(models.Model):
    tax_return_form = models.ForeignKey(Tax_Return_Form, on_delete=models.PROTECT, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    line = models.CharField(max_length=255, null=True, blank=True)
    instructions = models.CharField(max_length=255, null=True, blank=True)

class Tax_Return_Form_Line_Input(models.Model):
    tax_return_form_line = models.ForeignKey(Tax_Return_Form_Line, on_delete=models.PROTECT, null=True, blank=True)
    amount = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2, default=0.00, null=True, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)
