from django.shortcuts import render,redirect

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm

from .models import Profile

from django.contrib.auth.models import User

# Create your views here.

def register_view(request):

    if request.method == 'POST':

        form = UserRegisterForm(request.POST)
 

        if form.is_valid():

            user = form.save(commit=False)

            user.set_password(form.cleaned_data['password'])

            user.save()

            Profile.objects.create(user=user,role=form.cleaned_data['role'])

            return redirect('login')
        

    else :    

        form = UserRegisterForm()

    return render(request, 'users/register.html',{'form':form})    

def login_view(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(request,usename=username,password=password)

        if user is not None :

            login(request,user)

            profile= Profile.objects.get(user=user)


            if profile.role == 'doctor' :

                return redirect('doctor_dashboard')
            
            else :

                return redirect('patient_dashboard')
            
        else :

            return render(request,'users/login.html',{'error': 'Invalid credentials'})    
        
    return render(request,'users/login.html')

@login_required

def doctor_dashboard(request):

    return render(request,'user/doctor_dashboard.html')

@login_required

def patient_dashboard(request):

    return render(request,'user/patient_dashboard.html')

def logout_view(request):

    logout(request)

    return redirect('home')