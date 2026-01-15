from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpSelectionView.as_view(), name='signup_selection'),
    path('signup/doctor/', views.DoctorSignUpView.as_view(), name='doctor_signup'),
    path('signup/patient/', views.PatientSignUpView.as_view(), name='patient_signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='home'),
]
