from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        # If a next param is present, honor it (optional, check safety first)
        next_url = request.GET.get('next')
        if next_url and next_url.startswith('/'):
            return next_url

        user = request.user
        profile = getattr(user, 'userprofile', None)
        if profile and profile.is_employer:
            return reverse('users:employer_dashboard')
        else:
            return reverse('users:profile')
