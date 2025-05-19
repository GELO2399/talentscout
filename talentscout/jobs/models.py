from django.db import models
from django.contrib.auth.models import User
from users.models import UserProfile


class Job(models.Model):
    FULL_TIME = 'FT'
    PART_TIME = 'PT'
    HYBRID = 'HY'
    REMOTE = 'RM'

    JOB_TYPE_CHOICES = [
        (FULL_TIME, 'Full-time'),
        (PART_TIME, 'Part-time'),
        (HYBRID, 'Hybrid'),
        (REMOTE, 'Remote'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jobs_posted')
    applications = models.ManyToManyField(User, related_name='job_applications', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    requirements = models.TextField(blank=True, null=True)
    job_type = models.CharField(
        max_length=2, 
        choices=JOB_TYPE_CHOICES, 
        blank=True, 
        null=True
    )
    salary_range = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

    
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('job', 'applicant')
        ordering = ['-applied_at']