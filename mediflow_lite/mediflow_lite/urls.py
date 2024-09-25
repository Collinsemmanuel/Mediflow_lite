from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import PatientViewSet, DoctorViewSet, AppointmentViewSet, MedicalRecordViewSet

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'appointments', AppointmentViewSet)
router.register(r'medical-records', MedicalRecordViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # This line includes the core app's URLs
    path('api/', include(router.urls)),
]