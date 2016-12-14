import matplotlib.pyplot as plt
from finance.models import Charge, Account
import numpy as np
from django.db.models import Sum
from django.db.models.functions import TruncMonth, TruncYear
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import datetime


def getTotalLine (charges, account):
    # charges = list(Charge.objects.filter(account=account_number).order_by('-date'))
    # total = list(Account.objects.filter(account_number=account_number))
    total = account.total
    x = []
    y = []
    for charge in reversed(charges):
        x.append(charge.date)
        y.append(total)
        total -= charge.value
    filename = 'total.png'
    plt.figure(1)
    plt.clf()
    fig, ax = plt.subplots()
    plt.plot(x, y, 'bo')
    plt.plot(x, y, '-b')
    plt.margins(0.2)
    fig.autofmt_xdate()
    plt.title("Account: " + str(account.account_number))
    plt.savefig('static/img/total.png', format='png')
    return filename


def getTotalTable (account_number):
    acc = Account.objects.get(account_number=account_number)
    charges = list(Charge.objects.filter(account=acc.id)
                   .annotate(mon=TruncMonth('date'))
                   .values('mon')
                   .order_by('-mon')
                   .annotate(year=TruncYear('date'))
                   .annotate(subtotal=Sum('value'))
                   # .values('', 'subtotal')
                   )
    # print(charges)
    total = acc.total
    for charge in charges:
        charge['year'] = charge['year'].year
        charge['mon'] = charge['mon'].month
        temp = charge['subtotal']
        charge['subtotal'] = total
        total = total - temp
    print(charges)
    return charges

