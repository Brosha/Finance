from rest_framework import serializers
from finance.models import Account, Charge


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('name', 'total', 'account_number')


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = ('value', 'date', 'category')
