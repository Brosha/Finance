from rest_framework import serializers
from rest_framework.response import Response
from finance.models import Account, Charge


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('name', 'total', 'account_number')


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = ('value', 'date', 'category')


class StatisticsSerializer(serializers.Serializer):
    year = serializers.CharField(max_length=16)
    subtotal = serializers.DecimalField(max_digits=8, decimal_places=2)
    mon = serializers.CharField(max_length=16)

