from django.db import models
from decimal import Decimal

SERVICE_CHOICES = [
    ("videography", "Videography"), ("photography", "Photography"),
    ("branding", "Strategic Branding & Identity"), ("digital", "Digital Marketing & UI Solutions"),
]
PACKAGE_CHOICES = [
    ("silver", "Silver"), ("gold", "Gold"), ("platinum", "Platinum"),
    ("custom", "Custom / hourly"), ("studio", "Indoor studio shoot"),
    ("outdoor", "Outdoor / location shoot"), ("half_day", "Half-day event coverage"),
    ("full_day", "Full-day event coverage"), ("identity", "Visual corporate identity kit"),
    ("stationery", "Corporate stationery pack"), ("typography", "Typography & slogan branding"),
    ("web_mockups", "Responsive web interface mockups"), ("social_retainer", "Social media retainer strategy"),
    ("reels", "TikTok / Instagram Reels management"),
]
class Booking(models.Model):
    STATUS_CHOICES = [
        ("new", "New enquiry"), ("quoted", "Quote sent"), ("confirmed", "Confirmed"),
        ("in_production", "In production"), ("editing", "Editing"), ("ready", "Ready for delivery"),
        ("completed", "Completed"), ("cancelled", "Cancelled"),
    ]
    COVERAGE_CHOICES = [("nairobi", "Nairobi base studio"), ("kenya", "Country-wide Kenya travel"), ("international", "International project")]
    full_name = models.CharField(max_length=160)
    company_name = models.CharField(max_length=180, blank=True)
    contact_person = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=40)
    email = models.EmailField()
    services = models.JSONField(default=list)
    packages = models.JSONField(default=list)
    event_date = models.DateField(null=True, blank=True)
    venue = models.CharField(max_length=240, blank=True)
    coverage_zone = models.CharField(max_length=24, choices=COVERAGE_CHOICES, default="nairobi")
    details = models.TextField(blank=True)
    data_protection_consent = models.BooleanField(default=False)
    production_exclusivity_ack = models.BooleanField(default=False)
    financial_terms_ack = models.BooleanField(default=False)
    quote_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    deposit_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    balance_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    deposit_paid = models.BooleanField(default=False)
    balance_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=24, choices=STATUS_CHOICES, default="new")
    assigned_crew = models.CharField(max_length=240, blank=True)
    delivery_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ["-created_at"]
    def save(self, *args, **kwargs):
        self.deposit_amount = (self.quote_amount * Decimal("0.70")).quantize(Decimal("0.01"))
        self.balance_amount = (self.quote_amount * Decimal("0.30")).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.full_name} — {self.event_date or 'Date not set'}"

class ProductionTask(models.Model):
    booking = models.ForeignKey(Booking, related_name="tasks", on_delete=models.CASCADE)
    title = models.CharField(max_length=180)
    assigned_to = models.CharField(max_length=160, blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title
