from django.db import models

from django.contrib.auth.models import User

class Appointment(models.Model):
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')

    date = models.DateField()

    time = models.TimeField()

    reason = models.TextField(blank=True,null=True)

    STATUS_CHOICES = (
                      ('Pending','Pending'),
                      ('Approved','Approved'),
                      ('Completed','Completed'),
                      ('Cancelled','Cancelled'),
                      )

    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='Pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.patient.username} - {self.doctor.username}- {self.date} {self.time}"

