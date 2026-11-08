
from rest_framework.permissions import BasePermission, SAFE_METHODS


def get_user_role(user):
    if not user or not user.is_authenticated:
        return None

    if user.is_superuser:
        return "super_admin"

    try:
        return user.profile.role
    except Exception:
        return None


class IsStaffMember(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) in {
            "super_admin",
            "administrator",
            "production",
            "finance",
        }


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) in {
            "super_admin",
            "administrator",
        }


class IsFinanceStaff(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) in {
            "super_admin",
            "administrator",
            "finance",
        }


class IsProductionStaff(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) in {
            "super_admin",
            "administrator",
            "production",
        }


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return get_user_role(request.user) == "customer"


class IsOwnerOrStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        role = get_user_role(request.user)

        if role in {
            "super_admin",
            "administrator",
            "production",
            "finance",
        }:
            return True

        return (
            role == "customer"
            and getattr(obj, "customer_id", None) == request.user.id
        )
