from rest_framework import serializers

from .models import Doctor, Patient, Specialty


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ["id", "name"]


class PasswordHashingMixin:
    """Hache le mot de passe à la création et à la modification."""

    def create(self, validated_data):
        password = validated_data.pop("password")
        m2m = {k: validated_data.pop(k) for k in list(validated_data) if k == "specialties"}
        instance = self.Meta.model(**validated_data)
        instance.set_password(password)
        instance.save()
        for name, value in m2m.items():
            getattr(instance, name).set(value)
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance


class DoctorSerializer(PasswordHashingMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Doctor
        fields = ["id", "username", "password", "email", "first_name", "last_name",
                  "license_number", "phone", "specialties"]


class PatientSerializer(PasswordHashingMixin, serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Patient
        fields = ["id", "username", "password", "email", "first_name", "last_name",
                  "national_id", "phone", "birth_date"]