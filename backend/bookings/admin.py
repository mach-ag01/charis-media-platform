
from django.contrib import admin
from .models import Booking, ProductionTask, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "phone",
        "created_at",
    )
    list_filter = ("role",)
    search_fields = (
        "user__username",
        "user__email",
        "phone",
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "email",
        "event_date",
        "status",
        "quote_amount",
        "deposit_paid",
        "balance_paid",
    )
    list_filter = (
        "status",
        "coverage_zone",
        "event_date",
    )
    search_fields = (
        "full_name",
        "company_name",
        "email",
        "phone",
        "venue",
    )
    readonly_fields = ("created_at", "updated_at")


@admin.register(ProductionTask)
class ProductionTaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "booking",
        "assigned_to",
        "due_date",
        "completed",
    )
    list_filter = ("completed", "due_date")
