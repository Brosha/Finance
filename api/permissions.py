from rest_framework import permissions
from finance.models import Account


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user_id


class IsChargeOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        acc = Account.objects.get(pk=obj.account_id)
        return request.user.id == acc.user_id


