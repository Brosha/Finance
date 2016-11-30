from decimal import Decimal
from random import randint
from random import choice
import datetime
from datetime import date


def rounded(fn):

    def wrapped(*args, **kwargs):
        return round(Decimal(fn(*args, **kwargs)), 2)
    return wrapped


class Money(object):

    def __init__(self, value=0, is_editable=True):
        self.isEditable = is_editable
        self._value = value

    @rounded
    def get_value(self):
        return self._value

    def __str__(self):
        return str(self.get_value())


class Charge(object):

    def __init__(self, value=0, cause='Undefined', dateValue = date.today()):
        self._value = Money(is_editable=False, value=value)
        self._cause = cause
        self._date = dateValue

    @property
    def value(self):
        return self._value.get_value()

    @property
    def cause(self):
        return self._cause

    @property
    def date(self):
        return self._date


class Account(object):

    def __init__(self, total=0, charges=None):
        self._total = Money(is_editable=True, value=total)
        self._charges = list(charges)

    def append(self, charge):
        if self._total + charge > 0:
            temp_charge = Charge(charge)
            self._charges.append(temp_charge)
            self._total += charge
        else:
            raise ValueError('Your account value can not be negative')

    @property
    def get_total(self):
        return self._total.get_value()

    def __iter__(self):
        return iter(self._charges)

causes = ['Cacao', 'Candy', 'Ticket to 21 pilots', 'Box of otters', 'Sherlock\'s coat', 'Oscar for Leo', 'Movie ticket', 'Best car ever', 'Your dream soda', 'Dog food', 'Cat toys', 'Memes', 'X-men poster', 'Exams', 'Taxi to Paris', 'Best book ever', 'Donation for Leo', 'Save Mufasa','For environment needs', 'Mabel\'s sweater', 'Husky trip', 'Journy on turtles', 'For Pandas', 'Private plane','DOGE']


def random_transactions():
    today = date.today()
    start_date = today.replace(month=1, day=1).toordinal()
    end_date = today.toordinal()
    while True:
        start_date = randint(start_date, end_date)
        random_date = date.fromordinal(start_date)
        if random_date >= today:
            break
        random_value = randint(-10000, 10000), randint(0, 99)
        random_value = Decimal('%d.%d' % random_value)
        yield random_date, random_value


def random_account():
    charges = []
    for temp_date, temp_value in random_transactions():
        charges.append(Charge(value=temp_value, dateValue=temp_date, cause=choice(causes)))
    account = Account(total=randint(0, 10000), charges=charges)
    return account
