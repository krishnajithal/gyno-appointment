from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required

from users.models import Profile

def role_required(allowed_role):

    def decorator(view_func):

        @login_required

        def wrapper(request, *args, **kwargs):

            profile = Profile.objects.get(user=request.user)

            if profile.role != allowed_role:

                return redirect('login')   # OR 'home'

            return view_func(request, *args, **kwargs)
        
        return wrapper
    
    return decorator
