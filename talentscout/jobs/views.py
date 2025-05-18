from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Job, JobApplication
from .forms import JobForm
from users.models import UserProfile
from django.core.paginator import Paginator
from django.contrib import messages
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import logging
logger = logging.getLogger(__name__)

channel_layer = get_channel_layer()

def job_list(request):
    jobs = Job.objects.all().order_by('-posted_at')

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


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applicants = JobApplication.objects.filter(job=job)
    logger.info(f"Applicants found: {applicants}")
    print(f"Applicants found: {applicants}")
    return render(request, 'jobs/employer_job_detail.html', {
        'job': job,
        'applicants': applicants
    })

@login_required
def apply_job(request, job_id):
    if request.method == "POST":
        # Get the job object
        job = get_object_or_404(Job, id=job_id)
        
        try:
            # ✅ Get the UserProfile instance associated with the current user
            user_profile = UserProfile.objects.get(user=request.user)

            # ✅ Create the JobApplication
            JobApplication.objects.create(
                applicant=user_profile,
                job=job
            )
            messages.success(request, "You have successfully applied for the job!")
        except UserProfile.DoesNotExist:
            messages.error(request, "You do not have a profile yet. Please complete your profile first.")
            return redirect('users:profile')

    return redirect('jobs:job_detail', job_id=job_id)

@login_required
def employer_job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applicants = JobApplication.objects.filter(job=job)

    context = {
        'job': job,
        'applicants': applicants
    }
    return render(request, 'jobs/employer_job_detail.html', context)

@login_required
def accept_application(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    application.status = 'Accepted'
    application.save()

    # WebSocket notification
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"applicant_{application.applicant.id}", {
            'type': 'application_update',
            'message': 'Your application status was updated.',
            'status': 'Accepted',
            'job_id': application.job.id
        }
    )
    return redirect('jobs:employer_job_detail', job_id=application.job.id)

@login_required
def reject_applicant(request, application_id):
    application = get_object_or_404(JobApplication, id=application_id)
    application.status = 'rejected'
    application.save()

    # Send real-time update
    async_to_sync(channel_layer.group_send)(
        f'job_{application.job.id}',
        {
            'type': 'status_update',
            'status': 'rejected',
            'applicant': application.applicant.username
        }
    )

    messages.error(request, f"{application.applicant.username} has been rejected.")
    return redirect('jobs:employer_job_detail', job_id=application.job.id)