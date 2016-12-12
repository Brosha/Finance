from rest_framework import permissions
from finance.models import Account


class IsAccountOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return request.user.id == obj.user_id


class IsChargeOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        acc = Account.objects.get(pk=obj.account_id)
        return request.user.id == acc.user_id
