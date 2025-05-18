from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_employer = models.BooleanField(default=False)  # <--- New field for employers
    company_name = models.CharField(max_length=255, blank=True, null=True)
    skills = models.TextField(blank=True)  # comma separated
    experience = models.TextField(blank=True)
    education = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)

    def __str__(self):
        return self.user.username

