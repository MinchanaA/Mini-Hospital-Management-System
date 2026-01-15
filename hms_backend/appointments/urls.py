from django.urls import path
from . import views

urlpatterns = [
    path('add-availability/', views.add_availability, name='add_availability'),
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('book/<int:availability_id>/', views.book_appointment, name='book_appointment'),
]
