from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

def employer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.shortcuts import redirect
            return redirect('login')  # Redirect unauthenticated users to login
        if not request.user.groups.filter(name='Employers').exists():
            return HttpResponseForbidden("You do not have permission to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view
