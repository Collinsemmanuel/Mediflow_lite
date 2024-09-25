from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, Appointment, MedicalRecord


def home(request):
    return render(request, 'core/home.html')

@login_required
def patient_dashboard(request):
    patient = get_object_or_404(Patient, user=request.user)
    appointments = Appointment.objects.filter(patient=patient)
    medical_records = MedicalRecord.objects.filter(patient=patient)
    return render(request, 'patient_dashboard.html', {
        'patient': patient,
        'appointments': appointments,
        'medical_records': medical_records
    })

@login_required
def doctor_dashboard(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor)
    return render(request, 'doctor_dashboard.html', {
        'doctor': doctor,
        'appointments': appointments
    })

@login_required
def create_appointment(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        date_time = request.POST.get('date_time')
        reason = request.POST.get('reason')
        patient = get_object_or_404(Patient, user=request.user)
        doctor = get_object_or_404(Doctor, id=doctor_id)
        Appointment.objects.create(patient=patient, doctor=doctor, date_time=date_time, reason=reason)
        return redirect('patient_dashboard')
    doctors = Doctor.objects.all()
    return render(request, 'create_appointment.html', {'doctors': doctors})

@login_required
def create_medical_record(request):
    if request.method == 'POST':
        doctor_id = request.POST.get('doctor_id')
        notes = request.POST.get('notes')
        prescription = request.POST.get('prescription')
        patient = get_object_or_404(Patient, user=request.user)
        doctor = get_object_or_404(Doctor, id=doctor_id)
        MedicalRecord.objects.create(patient=patient, doctor=doctor, notes=notes, prescription=prescription)
        return redirect('patient_dashboard')
    doctors = Doctor.objects.all()
    return render(request, 'create_medical_record.html', {'doctors': doctors})

  
