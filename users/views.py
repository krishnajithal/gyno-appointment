from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages

from .forms import UserRegisterForm
from .models import Profile
from appointments.models import Appointment
from .decorators import role_required


# -----------------------------
# REGISTER VIEW
# -----------------------------
def register_view(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # Create profile
            Profile.objects.create(user=user, role=form.cleaned_data['role'])

            # SUCCESS MESSAGE AFTER REGISTRATION
            messages.success(request, "Account created successfully! Please login.")

            return redirect('login')

    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {
        'form': form,
        'hide_nav_links': True
    })


# -----------------------------
# LOGIN VIEW (IMPROVED ERRORS)
# -----------------------------
def login_view(request):

    error_message = None

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if username exists
        if not User.objects.filter(username=username).exists():
            error_message = "No account found with that username."
            return render(request, 'users/login.html', {'error': error_message})

        # Authenticate user
        user = authenticate(request, username=username, password=password)

        if user is None:
            error_message = "Incorrect password. Please try again."
            return render(request, 'users/login.html', {'error': error_message})

        # Login success
        login(request, user)
        profile = Profile.objects.get(user=user)

        if profile.role == 'doctor':
            messages.success(request, "Login successful! Welcome Doctor.")
            return redirect('doctor_dashboard')
        else:
            messages.success(request, "Login successful! Welcome Patient.")
            return redirect('patient_dashboard')
        
    return render(request, 'users/login.html')


# -----------------------------
# DOCTOR DASHBOARD
# -----------------------------
@role_required('doctor')
def doctor_dashboard(request):

    profile = Profile.objects.get(user=request.user)

    today = timezone.localdate()
    appointments = Appointment.objects.filter(doctor=request.user)

    context = {
        'total_appointments': appointments.count(),
        'today_count': appointments.filter(date=today).count(),
        'completed_count': appointments.filter(status='Completed').count(),

        'upcoming_appointments': appointments.filter(date__gt=today).order_by('date', 'time'),

        # NAVBAR FLAGS
        'hide_nav_links': False,
        'show_dashboard_link': False,
        'show_logout': True,
        'show_auth_links': False,
    }

    return render(request, 'users/doctor_dashboard.html', context)


# -----------------------------
# PATIENT DASHBOARD
# -----------------------------
@role_required('patient')
def patient_dashboard(request):

    profile = Profile.objects.get(user=request.user)

    today = timezone.localdate()
    appointments = Appointment.objects.filter(patient=request.user)

    context = {
        'total_appointments': appointments.count(),
        'upcoming_count': appointments.filter(date__gt=today).count(),
        'completed_count': appointments.filter(status='Completed').count(),

        'todays_appointments': appointments.filter(date=today),

        # NAVBAR FLAGS
        'hide_nav_links': False,
        'show_dashboard_link': False,
        'show_logout': True,
        'show_auth_links': False,
    }

    return render(request, 'users/patient_dashboard.html', context)


# -----------------------------
# LOGOUT VIEW
# -----------------------------
def logout_view(request):

    logout(request)

    messages.success(request, "You have logged out successfully.")

    return redirect('home')
