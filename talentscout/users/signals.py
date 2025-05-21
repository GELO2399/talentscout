# users/signals.py
from allauth.socialaccount.signals import pre_social_login
from allauth.exceptions import ImmediateHttpResponse
from django.dispatch import receiver
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import UserProfile
from allauth.account.signals import user_signed_up


@receiver(user_signed_up)
def create_user_profile(sender, request, user, **kwargs):
    # Create profile if not exist
    profile, created = UserProfile.objects.get_or_create(user=user)
    if created:
        # By default, mark as job seeker (not employer)
        profile.is_employer = False
        profile.save()

# Remove or comment out your old restrict_github_login_to_employers signal if you had one.
# This ensures both employers and job seekers can login via GitHub/social accounts.
