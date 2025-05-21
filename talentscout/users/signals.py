from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from users.models import UserProfile

@receiver(user_signed_up)
def create_user_profile(sender, request, user, **kwargs):
    profile, created = UserProfile.objects.get_or_create(user=user)
    if created:
        # Check session for 'social_role' flag
        role = request.session.get('social_role')
        if role == 'employer':
            profile.is_employer = True
        else:
            profile.is_employer = False
        profile.save()