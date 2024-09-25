from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='core_patient')
    date_of_birth = models.DateField()
    medical_history = models.TextField(blank=True)

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='core_doctor')
    specialty = models.CharField(max_length=100)

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled')
    ], default='SCHEDULED')

class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    notes = models.TextField()
    prescription = models.TextField(blank=True)
