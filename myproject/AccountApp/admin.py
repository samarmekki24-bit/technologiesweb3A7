from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Doctor, Patient, Specialty, User

admin.site.register(User, UserAdmin)


@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Doctor)
class DoctorAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'license_number', 'phone')
    search_fields = ('username', 'first_name', 'last_name', 'license_number')
    filter_horizontal = ('groups', 'user_permissions', 'specialties')

    fieldsets = UserAdmin.fieldsets + (
        ('Informations médecin', {'fields': ('license_number', 'phone', 'specialties')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations médecin', {'fields': ('license_number', 'phone', 'specialties')}),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        if obj:
            return (*readonly, 'license_number')
        return readonly


@admin.register(Patient)
class PatientAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'national_id', 'phone', 'birth_date')
    search_fields = ('username', 'first_name', 'last_name', 'national_id')

    fieldsets = UserAdmin.fieldsets + (
        ('Informations patient', {'fields': ('national_id', 'phone', 'birth_date')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informations patient', {'fields': ('national_id', 'phone', 'birth_date')}),
    )

    def get_readonly_fields(self, request, obj=None):
        readonly = super().get_readonly_fields(request, obj)
        if obj:
            return (*readonly, 'national_id')
        return readonly