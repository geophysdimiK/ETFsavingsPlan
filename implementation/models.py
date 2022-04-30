from django.db import models
from io import StringIO

# Create your models here.

class InvestmentAccount(models.Model):

    account_balance = models.FloatField()

    date = models.DateTimeField()


class InvestmentDeposit(models.Model):

    deposit_balance = models.FloatField()

    date = models.DateTimeField()


class Savings_Plan(models.Model):

    owners_name = models.CharField(max_length=50)

    transaction_fees = models.FloatField()

    administration_fees = models.FloatField()

    TER = models.FloatField()

    account = models.ForeignKey(
        InvestmentAccount, on_delete=models.CASCADE)

    deposit = models.ForeignKey(
        InvestmentDeposit, on_delete=models.CASCADE)
