from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Sum
from .models import Booking, ProductionTask
from .serializers import BookingSerializer, ProductionTaskSerializer
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get("status")
        if status: qs = qs.filter(status=status)
        return qs
class ProductionTaskViewSet(viewsets.ModelViewSet):
    queryset = ProductionTask.objects.select_related("booking").all()
    serializer_class = ProductionTaskSerializer
@api_view(["GET"])
def dashboard(request):
    bookings = Booking.objects.all()
    return Response({
        "total_bookings": bookings.count(),
        "new_enquiries": bookings.filter(status="new").count(),
        "active_projects": bookings.filter(status__in=["confirmed","in_production","editing"]).count(),
        "completed_projects": bookings.filter(status="completed").count(),
        "quoted_revenue": bookings.aggregate(total=Sum("quote_amount"))["total"] or 0,
        "pending_deposits": bookings.filter(deposit_paid=False).count(),
        "pending_balances": bookings.filter(balance_paid=False).count(),
        "status_breakdown": list(bookings.values("status").annotate(count=Count("id")).order_by("status")),
    })
