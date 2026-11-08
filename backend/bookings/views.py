
import logging

from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Count, Sum

from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Booking, ProductionTask
from .serializers import BookingSerializer, ProductionTaskSerializer


logger = logging.getLogger(__name__)


def send_booking_notification(booking):
    """Notify the Charis Media House owner of a new booking."""

    service_labels = {
        "videography": "Videography",
        "photography": "Photography",
        "branding": "Strategic Branding & Identity",
        "digital": "Digital Marketing & UI Solutions",
        "photomounts": "Photomounts",
    }

    package_labels = {
        "silver": "Silver",
        "gold": "Gold",
        "platinum": "Platinum",
        "custom": "Custom / hourly",
        "studio": "Indoor studio shoot",
        "outdoor": "Outdoor / location shoot",
        "half_day": "Half-day event coverage",
        "full_day": "Full-day event coverage",
        "identity": "Visual corporate identity kit",
        "stationery": "Corporate stationery pack",
        "typography": "Typography & slogan branding",
        "web_mockups": "Responsive web interface mockups",
        "social_retainer": "Social media retainer strategy",
        "reels": "TikTok / Instagram Reels management",
        "photomounts_a4_a0": "Photomounts (A4–A0)",
    }

    services = booking.services or []
    packages = booking.packages or []

    def readable_items(items, labels):
        return ", ".join(
            labels.get(item, str(item))
            if isinstance(item, str)
            else str(item)
            for item in items
        ) or "Not specified"

    subject = f"New Booking Enquiry #{booking.id} - Charis Media House"

    message = f"""
A new booking enquiry has been submitted.

BOOKING REFERENCE: #{booking.id}

CUSTOMER DETAILS
Name: {booking.full_name}
Company: {booking.company_name or "Not provided"}
Contact Person: {booking.contact_person or "Not provided"}
Phone: {booking.phone}
Email: {booking.email}

PROJECT DETAILS
Services: {readable_items(services, service_labels)}
Packages: {readable_items(packages, package_labels)}
Event Date: {booking.event_date or "Not specified"}
Venue: {booking.venue or "Not specified"}
Coverage: {booking.get_coverage_zone_display()}

Additional Requirements:
{booking.details or "No additional details provided"}

BOOKING STATUS
Status: {booking.get_status_display()}
Submitted: {booking.created_at}

Please log in to your administration dashboard to review this enquiry.
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.BOOKING_NOTIFICATION_EMAIL],
        fail_silently=False,
    )


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        status = self.request.query_params.get("status")

        if status:
            qs = qs.filter(status=status)

        return qs

    def perform_create(self, serializer):
        booking = serializer.save()

        try:
            send_booking_notification(booking)
        except Exception:
            logger.exception(
                "Booking #%s was saved, but its notification email failed.",
                booking.id,
            )


class ProductionTaskViewSet(viewsets.ModelViewSet):
    queryset = ProductionTask.objects.select_related("booking").all()
    serializer_class = ProductionTaskSerializer


@api_view(["GET"])
def dashboard(request):
    bookings = Booking.objects.all()

    return Response({
        "total_bookings": bookings.count(),
        "new_enquiries": bookings.filter(status="new").count(),
        "active_projects": bookings.filter(
            status__in=["confirmed", "in_production", "editing"]
        ).count(),
        "completed_projects": bookings.filter(status="completed").count(),
        "quoted_revenue": bookings.aggregate(
            total=Sum("quote_amount")
        )["total"] or 0,
        "pending_deposits": bookings.filter(deposit_paid=False).count(),
        "pending_balances": bookings.filter(balance_paid=False).count(),
        "status_breakdown": list(
            bookings.values("status")
            .annotate(count=Count("id"))
            .order_by("status")
        ),
    })
