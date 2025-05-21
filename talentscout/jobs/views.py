from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication
from .forms import JobForm
from users.models import UserProfile
from django.core.paginator import Paginator
from django.contrib import messages
import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.http import HttpResponse

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
    profile = getattr(request.user, 'userprofile', None)
    
    # Fetch job applications if the user is an employer and owns the job
    applications = None
    if profile and profile.is_employer and job.employer == request.user:
        applications = JobApplication.objects.filter(job=job)
    
    return render(request, 'jobs/job_detail.html', {
        'job': job,
        'profile': profile,
        'applications': applications,
    })


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    profile = getattr(request.user, 'userprofile', None)

    if not profile or profile.is_employer:
        messages.error(request, "Only job seekers can apply to jobs.")
        return redirect('jobs:job_detail', job_id=job_id)

    existing_application = JobApplication.objects.filter(job=job, applicant=profile).first()
    if existing_application:
        messages.info(request, "You have already applied to this job.")
    else:
        JobApplication.objects.create(job=job, applicant=profile)
        messages.success(request, "Your application has been submitted.")

    return redirect('jobs:job_detail', job_id=job_id)


@login_required
def employer_job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = job.jobapplication_set.all()

    if request.method == 'POST':
        action = request.POST.get('action')
        applicant_id = request.POST.get('applicant_id')

        if action == 'accept' and applicant_id:
            application = applications.get(applicant__id=applicant_id)
            application.status = 'accepted'
            application.save()

            # Notify WebSocket group
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f'job_{job_id}',
                {
                    'type': 'status_update',
                    'id': application.id,
                    'status': 'accepted',
                }
            )
            messages.success(request, f"{application.applicant.user.username} has been accepted.")

        return redirect('jobs:employer_job_detail', job_id=job_id)

    return render(request, 'jobs/employer_job_detail.html', {
        'job': job,
        'applicants': applications,  # renamed from 'applications' to 'applicants'
    })

def accept_job_application(request, job_id):
    if request.method == "POST":
        application = get_object_or_404(JobApplication, id=job_id)
        application.status = "accepted"
        application.save()
        return redirect('some_view_name')
    return HttpResponse("Invalid request", status=400)