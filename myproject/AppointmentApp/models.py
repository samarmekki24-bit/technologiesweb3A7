from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"

    doctor = models.ForeignKey(
        "AccountApp.Doctor",
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="praticien",
    )
    patient = models.ForeignKey(
        "AccountApp.Patient",
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="demandeur",
    )
    reason = models.TextField()
    prescription = models.FileField(
        upload_to="prescriptions/",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )
    duration_minutes = models.PositiveIntegerField(default=30)
    appointment_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date"],
                name="unique_doctor_appointment_date",
            )
        ]

    def clean(self):
        super().clean()
        if self.appointment_date and self.appointment_date <= timezone.now():
            raise ValidationError(
                {"appointment_date": "La date du rendez-vous doit être dans le futur."}
            )

    def __str__(self):
        return f"{self.patient} / {self.doctor} - {self.appointment_date:%d/%m/%Y %H:%M}"