"""
URL configuration for workshop3A7 project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from AccountApp.views import DoctorViewSet, PatientViewSet, SpecialtyViewSet
from AppointmentApp.views import AppointmentViewSet

router = DefaultRouter()
router.register("specialties", SpecialtyViewSet)
router.register("doctors", DoctorViewSet)
router.register("patients", PatientViewSet)
router.register("appointments", AppointmentViewSet)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)