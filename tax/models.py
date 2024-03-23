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
        return str(self.year) + ": " + str(self.payee) + "[" + str(self.id) + "]"

class Tax_Return_Form(models.Model):

    tax_return = models.ForeignKey(Tax_Return, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("tax:tax-return-detail", kwargs={"id": self.tax_return.id})

    def get_delete_url(self):
        return reverse("tax:tax-return-form-delete", kwargs={"id": self.id})

    def get_children(self):
        return self.tax_return_form_line_set.all()

    def __str__(self):
        return str(self.tax_return) + ">" + str(self.name) + "[" + str(self.id) + "]"

class Tax_Return_Form_Line(models.Model):
    tax_return_form = models.ForeignKey(Tax_Return_Form, on_delete=models.PROTECT, null=True, blank=True)
    number = models.CharField(max_length=255, null=True, blank=True)
    line = models.CharField(max_length=255, null=True, blank=True)
    instructions = models.CharField(max_length=255, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("tax:tax-return-form-detail", kwargs={"id": self.tax_return_form.id})

    def get_delete_url(self):
        return reverse("tax:tax-return-form-line-delete", kwargs={"id": self.id})

    def get_children(self):
        return self.tax_return_form_line_input_set.all()

    def get_line_amt(self):
        lsum = 0
        for c in self.tax_return_form_line_input_set.all():
            lsum += (c.inputvalue.amount * c.multiplier)
        return round(lsum, 2)

    def __str__(self):
        return str(self.tax_return_form) + ">" + str(self.number) + ">" + str(self.line) + "[" + str(self.id) + "]"

class DataSource(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("tax:datasource-list")

    def get_detail_url(self):
        return reverse("tax:datasource-detail", kwargs={"id": self.id})

    def get_edit_url(self):
        return reverse("tax:datasource-update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("tax:datasource-delete", kwargs={"id": self.id})

    def get_children(self):
        return self.inputvalue_set.all()

    def __str__(self):
        return str(self.name) + " [" + str(self.id) + "]"

class InputValue(models.Model):
    datasource = models.ForeignKey(DataSource, on_delete=models.PROTECT, null=True, blank=True)
    desc = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(verbose_name='Amount', max_digits=18, decimal_places=2, default=0.00, null=True, blank=True)
    text = models.CharField(max_length=255, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("tax:datasource-detail", kwargs={"id": self.datasource.id})

    def get_edit_url(self):
        return reverse("tax:inputvalue-update", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("tax:inputvalue-delete", kwargs={"id": self.id})

    def __str__(self):
        return str(self.datasource.name) + " " + str(self.desc)  +  "[" + str(self.id) + "]"


class Tax_Return_Form_Subtotal(models.Model):
    subtotal = models.CharField(max_length=100, null=True, blank=True)
    inputvalue = models.ForeignKey(InputValue, on_delete=models.PROTECT, null=True, blank=True)
    multiplier = models.DecimalField(max_digits=18, decimal_places=4, default=1.0000, null=True, blank=True)


class Tax_Return_Form_Line_Input(models.Model):
    tax_return_form_line = models.ForeignKey(Tax_Return_Form_Line, on_delete=models.PROTECT, null=True, blank=True)
    subtotal = models.ForeignKey(Tax_Return_Form_Subtotal, on_delete=models.PROTECT, null=True, blank=True)
    inputvalue = models.ForeignKey(InputValue, on_delete=models.PROTECT, null=True, blank=True)
    multiplier = models.DecimalField(max_digits=18, decimal_places=4, default=1.0000, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("tax:tax-return-form-line-detail", kwargs={"id": self.tax_return_form_line.id})

    def get_edit_url(self):
        return reverse("tax:tax-return-form-line-input-update")

    def get_amt(self):
        return round((self.inputvalue.amount * self.multiplier),2)

    def get_delete_url(self):
        return reverse("tax:tax-return-form-line-input-delete", kwargs={"id": self.id})

    def __str__(self):
        return str(self.tax_return_form_line) + "[" + str(self.id) + "]"