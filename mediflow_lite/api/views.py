from rest_framework import viewsets
from .models import Patient, Doctor, Appointment, MedicalRecord
from .serializers import PatientSerializer, DoctorSerializer, AppointmentSerializer, MedicalRecordSerializer
from groq import Groq

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        # Use Groq to define your query
        query = Groq("appointments")  # Adjust this based on your actual data structure
        # Fetch data using the query
        # This is a placeholder; you would need to implement the logic to execute the Groq query
        return self.queryset  # Return the queryset or the result of your Groq query

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer