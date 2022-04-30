from django.contrib import admin
from .models import Savings_Plan, InvestmentAccount, InvestmentDeposit

# Register your models here.
admin.site.register(Savings_Plan)

admin.site.register(InvestmentAccount)

admin.site.register(InvestmentDeposit)
