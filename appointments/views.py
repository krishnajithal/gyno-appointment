from django.shortcuts import render, redirect, get_object_or_404

from users.decorators import role_required

from .models import Appointment

from .forms import AppointmentForm

from users.models import Profile

from django.contrib import messages



@role_required('patient')

def create_appointment(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != 'patient':

        return redirect('home')

    if request.method == "POST":

        form = AppointmentForm(request.POST)

        if form.is_valid():

            appointment = form.save(commit=False)

            appointment.patient = request.user

            appointment.save()

            messages.success(request, "Appointment booked successfully!")

            return redirect('patient_appointment_list')
        
    else:

        form = AppointmentForm()

    return render(request, 'appointments/create_appointment.html', {
                                                                    'form': form,

                                                                    'show_dashboard_links': True,

                                                                    'show_logout': True,

                                                                    'title': 'Appointent Booking Page – GynoCare',

                                                                    })


@role_required('patient')

def patient_appointment_list(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != 'patient': 

        return redirect('home')

    appointments = Appointment.objects.filter(patient=request.user)

    return render(request, 'appointments/patient_appointment_list.html', {'appointments': appointments, 
                                                                          
                                                                          'show_dashboard_links': True,

                                                                          'show_logout': True,

                                                                          'title': 'My Appointents – GynoCare',
                                                                          })


@role_required('doctor')

def doctor_appointment_list(request):

    profile = Profile.objects.get(user=request.user)

    if profile.role != 'doctor':

        return redirect('home')

    appointments = Appointment.objects.all().order_by('-date', '-time')

    return render(request, 'appointments/doctor_appointment_list.html', {
                                                                        'appointments': appointments, 

                                                                        'show_dashboard_links': True,

                                                                        'show_logout': True,

                                                                        'title': 'All Appointents – GynoCare',
                                                                        })


@role_required('doctor')

def update_appointment_status(request, pk):

    profile = Profile.objects.get(user=request.user)

    if profile.role != 'doctor':

        return redirect('home')

    appointment = get_object_or_404(Appointment, id=pk)

    if request.method == "POST":

        new_status = request.POST.get('status')

        if new_status:

            appointment.status = new_status

            appointment.save()

            messages.success(request, "Appointment status updated successfully!")

            return redirect('doctor_appointment_list')

        else:
            return render(request, 'appointments/update_status.html', {
                                                                        'appointment': appointment,

                                                                        'error': 'Please select a status.',

                                                                        'show_dashboard_links': True,

                                                                        })

    return render(request, 'appointments/update_status.html', {
                                                                'appointment': appointment, 

                                                                'show_dashboard_link': False,

                                                                'show_logout': True,

                                                                'title': 'Status Update Page – GynoCare',

                                                                })

@role_required('patient')
def cancel_appointment(request, pk):

    profile = Profile.objects.get(user=request.user)

    if profile.role != "patient":

        return redirect("home")

    appointment = get_object_or_404(Appointment, id=pk, patient=request.user)

    appointment.status = "Cancelled"

    appointment.save()

    messages.success(request, "Appointment cancelled successfully!")

    return redirect('patient_appointment_list',{
                                                'show_dashboard_links': True, 

                                                'title': 'Cancel Appointment Page – GynoCare', 
                                                })

