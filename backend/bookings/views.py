
from django.db.models import Count, Sum

from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .models import Booking, ProductionTask
from .serializers import BookingSerializer, ProductionTaskSerializer
from .permissions import (
    get_user_role,
    IsOwnerOrStaff,
    IsStaffMember,
    IsProductionStaff,
)


class BookingViewSet(viewsets.ModelViewSet):
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Booking.objects.none()

        role = get_user_role(user)

        if role == "customer":
            return Booking.objects.filter(customer=user)

        if role in {
            "super_admin",
            "administrator",
            "production",
            "finance",
        }:
            return Booking.objects.all()

        return Booking.objects.none()

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]

        return [
            permissions.IsAuthenticated(),
            IsOwnerOrStaff(),
        ]

    def perform_create(self, serializer):
        user = self.request.user

        if user.is_authenticated and get_user_role(user) == "customer":
            serializer.save(customer=user)
        else:
            serializer.save()


class ProductionTaskViewSet(viewsets.ModelViewSet):
    serializer_class = ProductionTaskSerializer

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return ProductionTask.objects.none()

        role = get_user_role(user)

        if role in {"super_admin", "administrator", "production"}:
            return ProductionTask.objects.select_related("booking").all()

        return ProductionTask.objects.none()

    def get_permissions(self):
        return [IsProductionStaff()]


@api_view(["GET"])
@permission_classes([IsStaffMember])
def dashboard(request):
    role = get_user_role(request.user)

    bookings = Booking.objects.all()

    # Finance staff receive financial statistics.
    financial_data = {}

    if role in {"super_admin", "administrator", "finance"}:
        financial_data = {
            "quoted_revenue": bookings.aggregate(
                total=Sum("quote_amount")
            )["total"] or 0,

            "pending_deposits": bookings.filter(
                deposit_paid=False
            ).count(),

            "pending_balances": bookings.filter(
                balance_paid=False
            ).count(),
        }

    return Response({
        "total_bookings": bookings.count(),

        "new_enquiries": bookings.filter(
            status="new"
        ).count(),

        "active_projects": bookings.filter(
            status__in=["confirmed", "in_production", "editing"]
        ).count(),

        "completed_projects": bookings.filter(
            status="completed"
        ).count(),

        **financial_data,

        "status_breakdown": list(
            bookings.values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        ),
    })
