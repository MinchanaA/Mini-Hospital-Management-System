from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView, TemplateView
from .forms import DoctorSignUpForm, PatientSignUpForm
from .models import User
from .utils import send_email_async
from .utils import send_email_async

class SignUpSelectionView(TemplateView):
    template_name = 'registration/signup_selection.html'

class DoctorSignUpView(CreateView):
    model = User
    form_class = DoctorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Doctor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_email_async("SIGNUP_WELCOME", user.email, {"username": user.username, "role": "Doctor"})
        return redirect('dashboard')

class PatientSignUpView(CreateView):
    model = User
    form_class = PatientSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Patient'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_email_async("SIGNUP_WELCOME", user.email, {"username": user.username, "role": "Patient"})
        return redirect('dashboard')

from appointments.models import Availability, Appointment

def dashboard(request):
    context = {}
    if request.user.is_authenticated and request.user.is_doctor:
        context['availabilities'] = Availability.objects.filter(doctor=request.user).order_by('start_time')
    elif request.user.is_authenticated and request.user.is_patient:
        context['appointments'] = Appointment.objects.filter(patient=request.user).select_related('availability__doctor__doctor_profile').order_by('availability__start_time')
    else:
        return render(request, 'landing.html')
        
    return render(request, 'dashboard.html', context)
