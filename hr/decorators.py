# decorators.py

from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages
from .models import Hr

def is_hr(user):
    return user.is_authenticated and Hr.objects.filter(user=user).exists()

def hr_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not is_hr(request.user):
            messages.error(request, "You are not authorized to access this page.")
            return redirect('homepage')  # Replace 'homepage' with your actual homepage URL name
        return view_func(request, *args, **kwargs)
    return _wrapped_view