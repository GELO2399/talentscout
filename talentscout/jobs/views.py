from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication
from .forms import JobForm
from users.models import UserProfile
from django.core.paginator import Paginator
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)
@login_required
def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')


    # Filters
    query = request.GET.get('q')
    location = request.GET.get('location')
    job_type = request.GET.get('job_type')
    salary_min = request.GET.get('salary_min')

    if query:
        jobs = jobs.filter(title__icontains=query)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if salary_min:
        jobs = jobs.filter(salary_range__gte=salary_min)

    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'jobs/job_list.html', {'jobs': page_obj})


@login_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            return redirect('jobs:job_list')
    else:
        form = JobForm()
    return render(request, 'jobs/post_job.html', {'form': form})




@login_required
def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    profile = getattr(request.user, 'userprofile', None)  # your custom profile model
    
    # Fetch job applications if the user is an employer and owns the job
    applications = None
    if profile and profile.is_employer and job.employer == request.user:
        applications = JobApplication.objects.filter(job=job)
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'profile': profile,
        'applications': applications,  # will be None for job seekers
    })


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    profile = getattr(request.user, 'userprofile', None)

    if not profile or profile.is_employer:
        messages.error(request, "Only job seekers can apply to jobs.")
        return redirect('jobs:job_detail', job_id=job_id)

    # Create job application if not already applied
    existing_application = JobApplication.objects.filter(job=job, applicant=profile).first()
    if existing_application:
        messages.info(request, "You have already applied to this job.")
    else:
        JobApplication.objects.create(job=job, applicant=profile)
        messages.success(request, "Your application has been submitted.")

    return redirect('jobs:job_detail', job_id=job_id)

