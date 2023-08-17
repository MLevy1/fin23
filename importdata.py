from fin.models import Trans, Account, Payee, Category
import csv

with open("C:\\Users\\mslev\\iCloudDrive\\PFIN\\2023-07-13-v2-post-pay1_2.csv", newline='') as f:
    R = csv.reader(f)
    next(R)
    for r in R:
        x = Trans(tid=r[0], tdate=r[1], amount=r[4], account=Account(r[10]), payee=Payee(r[11]), category=Category(r[12]), match=r[9], oldCat=r[7], oldPayee=r[8])
        x.save()	