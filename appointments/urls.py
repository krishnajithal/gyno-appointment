from django.urls import path

from . import views

urlpatterns = [
    
    path('create/', views.create_appointment, name='create_appointment'),

    path('patient/list/', views.patient_appointment_list, name='patient_appointment_list'),

    path('doctor/list/', views.doctor_appointment_list, name='doctor_appointment_list'),

    path('update/<int:pk>/', views.update_appointment_status, name='update_status'),

]
