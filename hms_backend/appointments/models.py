from django.db import models
from users.models import User

class Availability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availabilities')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']
        verbose_name_plural = 'Availabilities'
        
    def __str__(self):
        return f"{self.doctor.username} - {self.start_time.strftime('%Y-%m-%d %H:%M')}"

class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    availability = models.OneToOneField(Availability, on_delete=models.CASCADE, related_name='appointment')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Appt: {self.patient.username} with {self.availability.doctor.username}"
