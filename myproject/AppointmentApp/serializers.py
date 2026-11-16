from django.utils import timezone
from rest_framework import serializers

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = ["id", "doctor", "patient", "reason", "prescription", "status",
                  "duration_minutes", "appointment_date", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

    def validate_appointment_date(self, value):
        # DRF n'appelle pas clean() du modèle : on répète la règle ici.
        if value <= timezone.now():
            raise serializers.ValidationError("La date du rendez-vous doit être dans le futur.")
        return value