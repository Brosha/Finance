from rest_framework import viewsets, status
from finance.models import Account, Charge
from api.serializers import AccountSerializer, ChargeSerializer
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from api.permissions import IsAccountOwner, IsChargeOwner


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


# def account_list(request):
#     if request.method == 'GET':
#         accounts = Account.objects.all()
#         serializer = AccountSerializer(accounts, many=True)
#         return JSONResponse(serializer.data)


# def charge_list(request):
#     if request.method == 'GET':
#         charges = Charge.objects.all()
#         serializer = ChargeSerializer(charges, many=True)
#         return JSONResponse(serializer.data)


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = (IsAdminUser, IsAccountOwner)

    def get_queryset(self):
        return Account.objects.filter(user_id=self.request.user.id)


class ChargeViewSet(viewsets.ModelViewSet):
    serializer_class = ChargeSerializer
    permission_classes = (IsAdminUser, IsChargeOwner)

    def get_queryset(self):
        return Charge.objects.filter(account_id__userid__exact=self.request.user.id)
