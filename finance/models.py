from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.CharField(max_length=11)
    address = models.CharField(max_length=100)


class Account(models.Model):

    name = models.CharField(max_length=100)
    total = models.DecimalField(decimal_places=2, max_digits=15)
    account_number = models.BigIntegerField()
    user = models.ForeignKey(User, related_name='+')

    def __str__(self):
        return str(self.account_number)

    class Meta:
        db_table = 'accounts'


class Charge(models.Model):
    value = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    category = models.CharField(max_length=100, blank=True)
    purpose = models.CharField(max_length=150, blank=True)
    account = models.ForeignKey(Account, related_name='+')

    class Meta:
        db_table = 'charges'


class Goal(models.Model):
    value = models.DecimalField(decimal_places=2, max_digits=10)
    goalValue = models.DecimalField(decimal_places=2, max_digits=10)
    date = models.DateField()
    category = models.CharField(max_length=100, blank=True)
    purpose = models.CharField(max_length=150, blank=True)
    account = models.ForeignKey(Account, related_name='+')

    class Meta:
        db_table = 'goals'
