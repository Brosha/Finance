from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from finance import controller
from decimal import Decimal
from datetime import date
from finance.models import Account, Charge
from finance.form_validation import ChargeForm, GetAccountsListForm, AccountForm, GoalForm, UserForm, LoginForm
from random import randint
from finance.statistics import getTotalLine, getTotalTable
from django.db import transaction
import csv


def home(request):
    if request.method == 'POST':
        form = GetAccountsListForm(request.POST)
        if form.is_valid():
            return redirect('status', form.cleaned_data.get('account').account_number)
    else:
        form = GetAccountsListForm()
    return render(request, 'home.html',
                  {'form': form})


def random_example(request):
    account = controller.random_account()
    return render(
        request, 'table.html',
        {'account': account}
    )


def send_total(request, account_id):
    charges = getTotalTable(account_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Totalstat.csv"'
    writer = csv.writer(response)
    writer.writerow(['Year', 'Month', 'Total'])
    for charge in charges:
        writer.writerow([charge['year'], charge['mon'], charge['subtotal']])
    return response


def total(request, account_id):
    acc = Account.objects.get(account_number=account_id)
    charges = list(Charge.objects.filter(account=acc.id).order_by('date'))
    file_name = getTotalLine(charges, acc)
    charges = getTotalTable(account_id)
    acc = Account.objects.get(account_number=account_id)
    return render(
        request, 'total_table.html',
        {'account': charges, 'account_id': account_id, 'acc': acc}
    )


def account_status(request, account_id=0):
    acc = Account.objects.get(account_number=account_id)
    charges = list(Charge.objects.filter(account=acc.id).order_by('date'))
    name = getTotalLine(charges, acc)
    #print(charges)
    return render(
        request, 'table.html',
        {'account': charges, 'account_id': account_id, 'acc': acc}
    )


def add_charge(request, account_id=0):
    if request.method == 'POST':
        form = ChargeForm(request.POST)
        info = 'Form is filled, but not correct'

        if form.is_valid():
            info = 'Form is filled and correct'
            #with transaction.atomic():
            acc = Account.objects.get(account_number=account_id)
            charg = form.save(commit=False)
            charg.account_id = acc.id
            tot = acc.total + charg.value
            if tot < 0:
                info = 'Account total can not be negative'
                form = ChargeForm(initial={'value': Decimal(100), 'date': date.today()})
                return render(
                    request, 'input.html',
                    {'form': form, 'info': info, 'account_id': account_id}
                )
            else:
                acc.total += charg.value
                acc.save()
                charg.save()
                return redirect('status', account_id)


    else:
        info = 'Form is not filled'
        form = ChargeForm(initial={'value': Decimal(100), 'date': date.today()})

    return render(
        request, 'input.html',
        {'form': form, 'info': info, 'account_id': account_id}
    )


def add_goal(request, account_id=0):
    if request.method == 'POST':
        form = GoalForm(request.POST)
        info = 'Form is filled, but not correct'

        if form.is_valid():
            info = 'Form is filled and correct'
            #with transaction.atomic():
            acc = Account.objects.get(account_number=account_id)
            goal = form.save(commit=False)
            goal.account_id = acc.id
            goal.date = date.today()
            goal.value = 0
            goal.save()
            return redirect('status', account_id)
    else:
        info = 'Form is not filled'
        form = GoalForm(initial={'goalValue': Decimal(100), 'purpose': str(140), 'category': str(140)})

    return render(
        request, 'add_goal.html',
        {'form': form, 'info': info, 'account_id': account_id}
    )


def add_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        info = 'Account is filled, but not correct'
        if form.is_valid():
            info = 'Account is filled and correct'
            with transaction.atomic():
                number = randint(0, 100000)
                acc = form.save(commit=False)
                acc.account_number = number
                acc.save()
                return redirect('status', number)
    else:
        info = 'Account is not filled'
        form = AccountForm()
    return render(
        request, 'accountinput.html',
        {'form': form, 'info': info}
        )


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        info = 'Account is filled, but not correct'
        if form.is_valid():
            info = 'Account is filled and correct'
            user = form.save()
            user.save()
    else:
        info = 'Account is not filled'
        form = UserForm()
    return render(
        request, 'register.html',
        {'form': form, 'info': info}
        )


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        info = 'Username and password are filled, but not correct'
        if form.is_valid():
            print(form.cleaned_data['username'])
            print(form.cleaned_data['password'])
            info = 'Username and password are filled and correct'
    else:
        info = 'Username and password are not filled'
        form = LoginForm()
    return render(
        request, 'login.html',
        {'form': form, 'info': info}
        )