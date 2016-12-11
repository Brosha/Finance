from rest_framework import viewsets
from finance.models import Account, Charge
from api.serializers import AccountSerializer, ChargeSerializer
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def account_list(request):
    if request.method == 'GET':
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return JSONResponse(serializer.data)


def charge_list(request):
    if request.method == 'GET':
        charges = Charge.objects.all()
        serializer = ChargeSerializer(charges, many=True)
        return JSONResponse(serializer.data)

# class AccountViewSet(viewsets.ModelViewSet):
#     queryset = Account.objects.all()
#     serializer_class = AccountSerializer
#
#
# class ChargeViewSet(viewsets.ModelViewSet):
#     queryset = Charge.objects.all()
#     serializer_class = ChargeSerializer
