from django import forms
from .models import Appointment
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class AppointmentForm(forms.ModelForm):

    class Meta:

        model = Appointment

        fields = ['doctor', 'date', 'time', 'reason']

        widgets = {
            'doctor': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'date': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'time': forms.TimeInput(
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'reason': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe your symptoms...'}
            ),
        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        #SHOW ONLY DOCTORS IN DROPDOWN
        doctors = User.objects.filter(profile__role='doctor')

        self.fields['doctor'].queryset = doctors

        self.fields['doctor'].label_from_instance = (
        lambda obj: f"Dr. {obj.username.capitalize()}"
        )


    def clean_date(self):

        selected_date = self.cleaned_data.get('date')

        if selected_date < timezone.now().date():

            raise ValidationError("You cannot select a past date.")

        return selected_date


    def clean_time(self):

        selected_time = self.cleaned_data.get('time')

        return selected_time


    def clean(self):

        cleaned_data = super().clean()

        doctor = cleaned_data.get('doctor')

        date = cleaned_data.get('date')

        time = cleaned_data.get('time')

        if doctor and date and time:

            exists = Appointment.objects.filter(

                doctor=doctor, date=date, time=time

            ).exists()

            if exists:

                raise ValidationError(

                    "The selected doctor already has an appointment at this time."
                )

        return cleaned_data
