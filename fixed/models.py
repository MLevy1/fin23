from django.db import models

from django.urls import reverse

from fin.models import (
	Payee,
	GroupedCat,
	Account
)

# Create your models here.
class Flow(models.Model):
    payee = models.ForeignKey(Payee, on_delete=models.PROTECT)
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    desc = models.CharField(max_length=255, null=True, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    #F4
    def get_absolute_url(self):
        return reverse("fixed:detail", kwargs={"id": self.id})

    #F3
    def get_edit_url(self):
        return reverse("fixed:update", kwargs={"id": self.id})

    #F6
    def get_delete_url(self):
        return reverse("fixed:delete", kwargs={"id": self.id})

    def get_flow_total(self):
        tsum = 0
        for t in self.flowitem_set.all():
            tsum += t.amount
        return tsum

    def get_flowitem_children(self):
        return self.flowitem_set.all()

    def __str__(self):
        t = str(self.desc) + " " + str(self.payee) + "[ " + str(self.id) + " ]"
        return str(t)

class FlowItem(models.Model):
    flow = models.ForeignKey(Flow, on_delete=models.PROTECT)
    groupedcat = models.ForeignKey(GroupedCat, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    note = models.CharField(max_length=255, null=True, blank=True)

    def get_absolute_url(self):
        return self.flow.get_absolute_url()

    #F7
    def get_delete_url(self):
        return reverse("fixed:item-delete", kwargs={"parent_id": self.flow.id, "id": self.id})

    #F5
    def get_hx_edit_url(self):
        kwargs = {
            "parent_id": self.flow.id,
            "id": self.id
        }
        return reverse("fixed:item_update_hx", kwargs=kwargs)
