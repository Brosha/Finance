# Register your models here.
from django.contrib import admin
from finance.models import User, Account, Charge, Goal


admin.site.register(User)
admin.site.register(Account)
admin.site.register(Charge)
admin.site.register(Goal)

