from django.contrib import admin
from .models import Appointment
class DoctorPerso(admin.StackedInline):
    model = Doctor


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_date', 'doctor', 'patient', 'status', 'duration_minutes')
    list_filter = ('status', 'doctor')
    search_fields = ('doctor__last_name', 'patient__last_name', 'reason')
    date_hierarchy = 'appointment_date'
    list_per_page = 2
    ordering = ('appointment_date',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Description / Ordonnance', {
            'fields': ('reason', 'status', 'prescription'),
        }),
        ('Date / Durée', {
            'fields': (('appointment_date', 'duration_minutes'),),
        }),
        ('Patient / Docteurs', {
            'fields': ('doctor', 'patient'),
        }),
        ('Planification', {
            'fields': ('created_at', 'updated_at'),
        }),
    )