from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

class CustomAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        user = request.user
        profile = getattr(user, 'userprofile', None)
        logger.info(f"Redirecting user {user.email} with is_employer={profile.is_employer if profile else 'None'}")
        if profile and profile.is_employer:
            return reverse('users:employer_dashboard')
        else:
            return reverse('users:profile')
