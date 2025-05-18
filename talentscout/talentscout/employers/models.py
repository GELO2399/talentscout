from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job

class Applicant(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    application_status = models.CharField(max_length=20, default='Pending')
    resume = models.FileField(upload_to='applicant_resumes/', null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} applied to {self.job.title}"
