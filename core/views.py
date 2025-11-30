from django.shortcuts import render,redirect

from users.models import Profile


def home(request):

    if request.user.is_authenticated:

        profile = Profile.objects.get(user=request.user)

        if profile.role == "doctor":

            return redirect('doctor_dashboard')
        
        else:

            return redirect('patient_dashboard')

    return render(request, 'core/home.html')

