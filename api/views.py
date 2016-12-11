from rest_framework import viewsets, status, views
from finance.models import Account, Charge
from api.serializers import AccountSerializer, ChargeSerializer, StatisticsSerializer
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from api.permissions import IsAccountOwner, IsChargeOwner
from finance.statistics import getTotalTable


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
    permission_classes = (IsAccountOwner, IsAuthenticated)

    def get_queryset(self):
        return Account.objects.filter(user_id=self.request.user.id)


class ChargeViewSet(viewsets.ModelViewSet):
    serializer_class = ChargeSerializer
    permission_classes = (IsAuthenticated, IsChargeOwner)

    def get_queryset(self):
        return Charge.objects.filter(account_id__userid__exact=self.request.user.id)


class StatisticsView(views.APIView):
    permission_classes = (IsAccountOwner, IsAuthenticated)

    def get(self, request, pk=None, format=None):
        acc = Account.objects.get(account_number=pk)
        self.check_object_permissions(request, acc)
        charges = getTotalTable(pk)
        serializer = StatisticsSerializer(charges, many=True)
        return Response(serializer.data)
