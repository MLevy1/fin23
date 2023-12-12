from django.db import models

from fin.models import Category

# Create your models here.
class BudgetedItem(models.Model):

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
    itemCat = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    
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