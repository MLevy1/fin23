from django.db import models
from django.urls import reverse

# Create your models here.
class fcflow(models.Model):
    desc = models.CharField(max_length=50)
    ann_freq = models.IntegerField()
    amount = models.DecimalField(max_digits=18, decimal_places=2)

    def get_absolute_url(self):
        return reverse("proj:list")

    def get_ann_amt(self):
        return self.ann_freq * self.amount

    class Meta:

        ordering = ['-amount']
