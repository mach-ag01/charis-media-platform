from django.db import migrations, models
import django.db.models.deletion
from decimal import Decimal

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=160)),
                ("company_name", models.CharField(blank=True, max_length=180)),
                ("contact_person", models.CharField(blank=True, max_length=160)),
                ("phone", models.CharField(max_length=40)),
                ("email", models.EmailField(max_length=254)),
                ("services", models.JSONField(default=list)),
                ("packages", models.JSONField(default=list)),
                ("event_date", models.DateField(blank=True, null=True)),
                ("venue", models.CharField(blank=True, max_length=240)),
                ("coverage_zone", models.CharField(choices=[("nairobi","Nairobi base studio"),("kenya","Country-wide Kenya travel"),("international","International project")], default="nairobi", max_length=24)),
                ("details", models.TextField(blank=True)),
                ("data_protection_consent", models.BooleanField(default=False)),
                ("production_exclusivity_ack", models.BooleanField(default=False)),
                ("financial_terms_ack", models.BooleanField(default=False)),
                ("quote_amount", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12)),
                ("deposit_amount", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12)),
                ("balance_amount", models.DecimalField(decimal_places=2, default=Decimal("0.00"), max_digits=12)),
                ("deposit_paid", models.BooleanField(default=False)),
                ("balance_paid", models.BooleanField(default=False)),
                ("status", models.CharField(choices=[("new","New enquiry"),("quoted","Quote sent"),("confirmed","Confirmed"),("in_production","In production"),("editing","Editing"),("ready","Ready for delivery"),("completed","Completed"),("cancelled","Cancelled")], default="new", max_length=24)),
                ("assigned_crew", models.CharField(blank=True, max_length=240)),
                ("delivery_link", models.URLField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="ProductionTask",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)),
                ("assigned_to", models.CharField(blank=True, max_length=160)),
                ("due_date", models.DateField(blank=True, null=True)),
                ("completed", models.BooleanField(default=False)),
                ("notes", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("booking", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="tasks", to="bookings.booking")),
            ],
        ),
    ]
