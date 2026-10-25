from rest_framework import serializers
from .models import Booking, ProductionTask

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "deposit_amount", "balance_amount")

    def validate(self, attrs):
        required = ("data_protection_consent", "production_exclusivity_ack", "financial_terms_ack")
        for key in required:
            value = attrs.get(key, getattr(self.instance, key, False) if self.instance else False)
            if not value:
                raise serializers.ValidationError({key: "This acknowledgement is required before submitting."})
        return attrs

class ProductionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionTask
        fields = "__all__"
