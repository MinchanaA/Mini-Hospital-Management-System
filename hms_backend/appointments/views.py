from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from .forms import AvailabilityForm
from .models import Availability, Appointment
from users.models import User, DoctorProfile
from users.utils import send_email_async
from .calendar_utils import create_calendar_event

@login_required
def add_availability(request):
    if not request.user.is_doctor:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            availability = form.save(commit=False)
            availability.doctor = request.user
            availability.save()
            return redirect('dashboard')
    else:
        form = AvailabilityForm()
    
    return render(request, 'appointments/add_availability.html', {'form': form})

@login_required
def doctor_list(request):
    doctors = User.objects.filter(is_doctor=True).select_related('doctor_profile')
    return render(request, 'appointments/doctor_list.html', {'doctors': doctors})

@login_required
def book_appointment(request, availability_id):
    if not request.user.is_patient:
        messages.error(request, "Only patients can book appointments.")
        return redirect('dashboard')

    with transaction.atomic():
        # Select for update to lock the row and prevent race conditions
        availability = get_object_or_404(Availability.objects.select_for_update(), id=availability_id)
        
        if availability.is_booked:
            messages.error(request, "This slot has already been booked.")
            return redirect('doctor_list')
        
        # Create appointment and mark availability as booked
        Appointment.objects.create(patient=request.user, availability=availability)
        availability.is_booked = True
        availability.save()
        
        messages.success(request, "Appointment booked successfully!")
        
        # Trigger Integrations
        appt_info = {
            "doctor": availability.doctor.username,
            "patient": request.user.username,
            "time": availability.start_time.strftime("%Y-%m-%d %H:%M")
        }
        
        # 1. Send Email to Patient
        send_email_async("BOOKING_CONFIRMATION", request.user.email, appt_info)
        
        # 2. Sync with Google Calendar
        create_calendar_event(
            summary=f"Appointment: {request.user.username} with Dr. {availability.doctor.username}",
            start_time=availability.start_time,
            end_time=availability.end_time,
            attendees=[request.user.email, availability.doctor.email]
        )
        
    return redirect('dashboard')
