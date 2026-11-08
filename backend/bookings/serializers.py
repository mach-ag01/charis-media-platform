
from rest_framework import serializers

from .models import Booking, ProductionTask
from .permissions import get_user_role


class BookingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = "__all__"

        read_only_fields = (
            "id",
            "customer",
            "deposit_amount",
            "balance_amount",
            "created_at",
            "updated_at",
        )

    def get_fields(self):
        fields = super().get_fields()

        request = self.context.get("request")
        role = get_user_role(request.user) if request else None

        # Fields that public visitors and customers cannot modify.
        protected_fields = {
            "quote_amount",
            "deposit_paid",
            "balance_paid",
            "status",
            "assigned_crew",
            "delivery_link",
        }

        # Only authorized financial staff can manage financial records.
        if role not in {"super_admin", "administrator", "finance"}:
            protected_fields.add("quote_amount")
            protected_fields.add("deposit_paid")
            protected_fields.add("balance_paid")

        # Production staff can update project progress and delivery details.
        if role not in {"super_admin", "administrator", "production"}:
            protected_fields.add("status")
            protected_fields.add("assigned_crew")
            protected_fields.add("delivery_link")

        for field_name in protected_fields:
            if field_name in fields:
                fields[field_name].read_only = True

        return fields

    def validate(self, attrs):
        required = (
            "data_protection_consent",
            "production_exclusivity_ack",
            "financial_terms_ack",
        )

        for key in required:
            value = attrs.get(
                key,
                getattr(self.instance, key, False)
                if self.instance else False,
            )

            if not value:
                raise serializers.ValidationError({
                    key: "This acknowledgement is required."
                })

        return attrs


class ProductionTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductionTask
        fields = "__all__"
        read_only_fields = ("id", "created_at")
