from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def employer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'userprofile') or not request.user.userprofile.is_employer:
            messages.error(request, "Access denied: Employers only.")
            return redirect('users:profile')  # Redirect to user profile or somewhere safe
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def jobseeker_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'userprofile') or request.user.userprofile.is_employer:
            messages.error(request, "Access denied: Job seekers only.")
            return redirect('users:employer_dashboard')  # Redirect to employer dashboard or somewhere safe
        return view_func(request, *args, **kwargs)
    return _wrapped_view
