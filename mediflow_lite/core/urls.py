from django.urls import path
from .views import patient_dashboard, doctor_dashboard, create_appointment, create_medical_record, home

urlpatterns = [
    path('', home, name='home'),  # Add this line for the home view
    path('patient/dashboard/', patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('appointment/create/', create_appointment, name='create_appointment'),
    path('medical-record/create/', create_medical_record, name='create_medical_record'),
]
