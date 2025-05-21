# users/signals.py
from allauth.socialaccount.signals import pre_social_login
from allauth.exceptions import ImmediateHttpResponse
from django.dispatch import receiver
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import UserProfile

@receiver(pre_social_login)
def restrict_github_login_to_employers(sender, request, sociallogin, **kwargs):
    # Skip if user is already logged in
    if request.user.is_authenticated:
        return

    # Only restrict GitHub
    if sociallogin.account.provider != 'github':
        return

    # Get the email from GitHub account data
    email = sociallogin.account.extra_data.get('email')
    if not email:
        messages.error(request, "Unable to identify user via GitHub.")
        raise ImmediateHttpResponse(redirect(reverse('users:employer-login')))

    try:
        user = User.objects.get(email=email)
        # Check if this user has a profile and is an employer
        if not hasattr(user, 'userprofile') or not user.userprofile.is_employer:
            messages.error(request, "GitHub login is allowed only for employer accounts.")
            raise ImmediateHttpResponse(redirect(reverse('users:employer-login')))
    except User.DoesNotExist:
        # Block new GitHub signups (optional)
        messages.error(request, "GitHub login is allowed only for existing employer accounts.")
        raise ImmediateHttpResponse(redirect(reverse('users:employer-login')))
