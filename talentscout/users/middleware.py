from django.shortcuts import redirect
from django.contrib import messages

class EmployerOnlyMiddleware:
    """
    Middleware to prevent non-employers from accessing the employer dashboard,
    and capture 'role' from login requests for social logins.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Capture role (e.g., ?role=employer) during login
        role = request.GET.get('role')
        if role:
            request.session['social_role'] = role

        # Restrict access to employer dashboard
        if request.path.startswith('/users/employer-dashboard/'):
            if not request.user.is_authenticated or not request.user.userprofile.is_employer:
                messages.error(request, "You are not authorized to view this page.")
                return redirect('users:profile')

        return self.get_response(request)
