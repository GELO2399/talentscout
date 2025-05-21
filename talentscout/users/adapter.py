from allauth.account.adapter import DefaultAccountAdapter
from django.shortcuts import redirect
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        profile = getattr(user, 'userprofile', None)

        if profile and profile.is_employer:
            return reverse('users:employer_dashboard')
        return reverse('users:profile')