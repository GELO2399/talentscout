from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        profile = getattr(user, 'userprofile', None)

        # Session-based override for employer login
        if request.session.pop('login_as_employer', False):
            if profile and profile.is_employer:
                return reverse('users:employer_dashboard')

        if profile and profile.is_employer:
            return reverse('users:employer_dashboard')
        return reverse('users:profile')
