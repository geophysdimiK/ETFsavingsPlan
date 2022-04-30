#Make the necessary imports
from django.contrib.auth.models import User
from celery import shared_task
from .models import InvestmentAccount, InvestmentDeposit, Portfolio, Savings_Plan
import numpy as np
import time
from datetime import datetime
from django.db import connection
from yahoo_fin import stock_info

def download_data():

#denote the ticker 
    stock = 'SMICHA.SW'

#get the price through the function get_live_price from yahoo finance
    price = stock_info.get_live_price(stock)

    return price


def buy(amount):

    #If current day is not a trading day --> differentiate btw. Saturday and Sunday

    #Case Saturday (corresponding to weekday == 5)

    if (datetime.today().weekday() == 5):

        time_now = datetime.now()

        later_time = datetime(time_now.year, time_now.month, time_now.day+2, 9, 15)

        #Let the program sleep unti next Monday 9.15 am CH time

        time.sleep((later_time - time_now).total_seconds())

        #Subtract the (net) account balance and add the calculated ETF shares to deposit balance

        p = InvestmentAccount.objects.all().last()

        q = InvestmentAccount(account_balance=p.account_balance - amount, date=datetime.now())

        q.save()

        # Retrieve the ETF's price in Swiss Francs (CHF)
        price = download_data()

        P = InvestmentDeposit.objects.all().last()

        # Calculate the amount of ETF shares
        shares = amount / price

        Q = InvestmentDeposit(deposit_balance=P.deposit_balance+shares, date=datetime.now())

        Q.save()


    # Do the similar procedure for Sunday, i.e., weekday == 6

    elif (datetime.today().weekday() == 6):

        time_now = datetime.now()

        later_time = datetime(time_now.year, time_now.month, time_now.day+1, 9, 15)

        #Let the program sleep unti next Monday 9.15 am CH time

        time.sleep((later_time - time_now).total_seconds())

        #Subtract the (net) account balance and add the calculated ETF shares to deposit balance

        p = InvestmentAccount.objects.all().last()

        q = InvestmentAccount(account_balance=p.account_balance - amount, date=datetime.now())

        q.save()

        # Retrieve the ETF's price in Swiss Francs (CHF)
        price = download_data()

        P = InvestmentDeposit.objects.all().last()

        # Calculate the amount of ETF shares
        shares = amount / price

        Q = InvestmentDeposit(deposit_balance=P.deposit_balance+shares, date=datetime.now())

        Q.save()

    else:

        p = InvestmentAccount.objects.all().last()

        q = InvestmentAccount(account_balance=p.account_balance - amount, date=datetime.now())

        q.save()

        # Retrieve the ETF's price in Swiss Francs (CHF)
        price = download_data()

        P = InvestmentDeposit.objects.all().last()

        # Calculate the amount of ETF shares
        shares = amount / price

        Q = InvestmentDeposit(deposit_balance=P.deposit_balance+shares, date=datetime.now())

        Q.save()
        


@shared_task(bind=True)
def invest(self, savings_rate):

    #Here: retrieve the transaction fees from the savings plan
    S = Savings_Plan.objects.all().last()
    
    t = S.transaction_fees

    p = InvestmentAccount.objects.all().last()

    q = InvestmentAccount(account_balance=p.account_balance + savings_rate, date=datetime.now())

    q.save()

    if (q.account_balance > 50):

        #Calculate net investment amount (account balance - transaction fees)

        q.account_balance *= (1 - t/100)

        q.save()

        amount = q.account_balance

        buy(amount)

