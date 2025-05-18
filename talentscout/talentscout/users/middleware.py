# users/middleware.py
from django.shortcuts import redirect
from django.contrib import messages

class EmployerOnlyMiddleware:
    """
    Middleware to prevent non-employers from accessing the employer dashboard.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/users/employer-dashboard/'):
            if not request.user.is_authenticated or not request.user.userprofile.is_employer:
                messages.error(request, "You are not authorized to view this page.")
                return redirect('users:profile')
        response = self.get_response(request)
        return response
