from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from finance import controller
from decimal import Decimal
from datetime import date
from finance.models import Account, Charge, User, Goal
from finance.form_validation import ChargeForm, GetAccountsListForm, AccountForm, GoalForm, UserForm, LoginForm,\
    AddCashToGoal, EditProfile
from random import randint
from finance.statistics import getTotalLine, getTotalTable
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import error
from django.contrib.auth.decorators import login_required
import csv


#This decorator is checking user
def user_check(view):
    def wrapped(request, account_id, *args, **kwargs):
        acc = Account.objects.get(account_number=account_id)
        if request.user.id == acc.user_id or request.user.is_superuser:
            return view(request, account_id, *args, **kwargs)
        else:
            return HttpResponseRedirect('/login/')
    return wrapped


def home(request):
    return render(request, 'home.html')


def random_example(request):
    account = controller.random_account()
    return render(
        request, 'exampletable.html',
        {'account': account}
    )


@user_check
@login_required(login_url='login')
def send_total(request, account_id):
    acc = Account.objects.get(account_number=account_id)
    if request.user.id == acc.user_id:
        charges = getTotalTable(account_id)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Totalstat.csv"'
        writer = csv.writer(response)
        writer.writerow(['Year', 'Month', 'Total'])
        for charge in charges:
            writer.writerow([charge['year'], charge['mon'], charge['subtotal']])
        return response
    else:
        return HttpResponseRedirect('/')


@user_check
@login_required(login_url='login')
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


@user_check
@login_required(login_url='login')
def account_status(request, account_id=0):
    acc = Account.objects.get(account_number=account_id)
    charges = list(Charge.objects.filter(account=acc.id).order_by('date'))
    name = getTotalLine(charges, acc)
    #print(charges)
    return render(
        request, 'table.html',
        {'account': charges, 'account_id': account_id, 'acc': acc}
    )


@user_check
@login_required(login_url='login')
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


@user_check
@login_required(login_url='login')
def account_goal_status(request, account_id=0):
    acc = Account.objects.get(account_number=account_id)
    if request.user.id == acc.user_id:
        goals = list(Goal.objects.filter(account=acc.id).order_by('date'))
        return render(
            request, 'goals.html',
            {'account': goals, 'account_id': account_id, 'acc': acc}
        )
    else:
        return HttpResponseRedirect('/')


@user_check
@login_required(login_url='login')
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
            return redirect('goals', account_id)
    else:
        info = 'Form is not filled'
        form = GoalForm(initial={'goalValue': Decimal(100), 'purpose': 'Your purpose', 'category': 'Your category'})

    return render(
        request, 'add_goal.html',
        {'form': form, 'info': info, 'account_id': account_id}
    )


@user_check
@login_required(login_url='login')
def add_value_goal(request, account_id=0, goal_id=0):
    if request.method == 'POST':
        form = AddCashToGoal(request.POST)
        info = 'goal form is filled, but not correct'
        if form.is_valid():
            info = 'goal form is filled and correct'
            goal = Goal.objects.get(pk=goal_id)
            val = form.cleaned_data['addvalue']
            goal.value += val
            if goal.value >= goal.goalValue:
                charge = Charge.objects.create(value=goal.value,
                                               date=date.today(),
                                               account=goal.account,
                                               category=goal.category,
                                               purpose=goal.purpose)
                acc = Account.objects.get(account_number=account_id)
                acc.total += goal.value
                acc.save()
                charge.save()
                goal.delete()
            else:
                goal.save()
            return redirect('goals', account_id)
    else:
        info = 'goal form is not filled'
        form = AddCashToGoal()
    return render(
        request, 'add_value_to_goal.html',
        {'form': form, 'info': info, 'goal_id': goal_id, 'account_id': account_id}
        )


@login_required(login_url='login')
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
                acc.user_id = request.user.id
                acc.save()
                return redirect('status', number)
    else:
        info = 'Account is not filled'
        form = AccountForm()
    return render(
        request, 'accountinput.html',
        {'form': form, 'info': info}
        )


@user_check
@login_required(login_url='login')
def edit_account(request, account_id=0):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        info = 'Account is filled, but not correct'
        if form.is_valid():
            acc = Account.objects.get(account_number=account_id)
            acc.total = form.cleaned_data['total']
            acc.name = form.cleaned_data['name']
            acc.save()
            return redirect('profile')
    else:
        info = 'Account is not filled'
        form = AccountForm()
    return render(
        request, 'account_edit.html',
        {'form': form, 'info': info, 'account_id': account_id}
        )


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        info = 'Account is filled, but not correct'
        if form.is_valid():
            info = 'Account is filled and correct'
            # user = form.save()
            # user.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            phone = form.cleaned_data['phone_number']
            print(form.cleaned_data)
            user = User.objects.create_user(username=username,
                                            password=password,
                                            address=address,
                                            phone_number=phone
                                            )
            user.save()
            return redirect('/')
    else:
        info = 'Account is not filled'
        form = UserForm()
    return render(
        request, 'register.html',
        {'form': form, 'info': info}
        )


@login_required(login_url='login')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfile(request.POST)
        info = 'Account is filled, but not correct'
        if form.is_valid():
            info = 'Account is filled and correct'
            olduser = User.objects.get(pk=request.user.id)
            if form.cleaned_data['username'] is not "":
                olduser.username = form.cleaned_data['username']
            if form.cleaned_data['password'] is not "":
                olduser.set_password(form.cleaned_data['password'])
            olduser.address = form.cleaned_data['address']
            olduser.phone = form.cleaned_data['phone_number']
            print(form.cleaned_data)
            olduser.save()
            return redirect('/')
    else:
        info = 'Account is not filled'
        form = EditProfile()
    return render(
        request, 'editprofile.html',
        {'form': form, 'info': info}
        )


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        info = 'Username and password are filled, but not correct'
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username)
            print(password)
            if not (username and password):
                print('Username or password is null')
                return render(request, 'login.html', {'form': form, 'info': info})
            user = authenticate(username=username, password=password)
            if not user:
                print('login error!!!')
                error(request, 'Wrong credentials!')
                return render(request, 'login.html', {'form': form, 'info': info})
            login(request, user)
            request.session.set_expiry(300)
            request.session['user_id'] = user.id
            info = 'Username and password are filled and correct'
            return redirect('/profile')
    else:
        info = 'Username and password are not filled'
        form = LoginForm()
    return render(
        request, 'login.html',
        {'form': form, 'info': info}
        )


@login_required(login_url='login')
def profile(request):

    #user_id = request.session['user_id']
    user_id = request.user.id

    accounts=Account.objects.filter(user=user_id)
    print(user_id)

        #form.fields['account'].queryset = Account.objects.get(user_id=user_id)
    return render(request, 'profile.html',
                  { 'user_id': user_id, 'accounts':accounts})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')



