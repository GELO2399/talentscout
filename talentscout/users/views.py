from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserProfileForm, EmployerSignupForm
from .models import UserProfile, Skill
from pyresparser import ResumeParser
from jobs.models import JobApplication, Job
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib.auth.models import User
from users.decorators import employer_required, jobseeker_required
import os

# ------------------------------
# 🟢 User Profile View
# ------------------------------
@login_required
@jobseeker_required
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            instance = form.save()
            if instance.resume:
                path = instance.resume.path
                try:
                    data = ResumeParser(path).get_extracted_data()
                    instance.skills.set([Skill.objects.get_or_create(name=skill)[0] for skill in data.get('skills', [])])
                    instance.experience = data.get('experience', '')
                    instance.education = ', '.join(data.get('education', []))
                    instance.save()
                except Exception as e:
                    print('Resume parsing failed:', e)
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'users/profile.html', {'form': form})

# ------------------------------
# 🟢 Employer Signup View
# ------------------------------
def employer_signup(request):
    if request.method == 'POST':
        form = EmployerSignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            company_name = form.cleaned_data.get('company_name')

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists. Please choose a different username.")
                return render(request, 'users/employer_signup.html', {'form': form})

            user = User.objects.create_user(username=username, password=password, email=email)
            user.userprofile.is_employer = True
            user.userprofile.company_name = company_name
            user.userprofile.save()

            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            messages.success(request, "Employer account created successfully!")
            return redirect('users:employer_dashboard')
    else:
        form = EmployerSignupForm()
    return render(request, 'users/employer_signup.html', {'form': form})

# ------------------------------
# 🟢 Employer Dashboard View
# ------------------------------
@login_required
@employer_required
def employer_dashboard(request):
    profile = UserProfile.objects.get(user=request.user)
    jobs = Job.objects.filter(employer=request.user).annotate(applications_count=Count('jobapplication')).order_by('-created_at')

    # Optional filters
    query = request.GET.get('q')
    location = request.GET.get('location')
    job_type = request.GET.get('job_type')

    if query:
        jobs = jobs.filter(title__icontains=query)
    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type=job_type)

    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'users/employer_dashboard.html', {
        'jobs': page_obj,
        'profile': profile,
    })

# ------------------------------
# 🟢 Employer Login View
# ------------------------------
def employer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            profile = getattr(user, 'userprofile', None)
            if profile and profile.is_employer:
                login(request, user)
                return redirect('users:employer_dashboard')
            else:
                messages.error(request, "This account is not registered as an employer.")
        else:
            messages.error(request, "Invalid credentials.")
    return render(request, 'users/employer_login.html')
# ------------------------------
# 🟢 Apply for Job View
# ------------------------------
@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    profile = getattr(request.user, 'userprofile', None)

    if not profile or profile.is_employer:
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect('jobs:job_detail', job_id=job_id)

    application, created = JobApplication.objects.get_or_create(job=job, applicant=profile)
    if created:
        messages.success(request, "You have successfully applied for the job.")
    else:
        messages.info(request, "You have already applied for this job.")
    return redirect('jobs:job_detail', job_id=job_id)

# ------------------------------
# 🟢 Employer Job Detail View
# ------------------------------
@login_required
def employer_job_detail(request, job_id):
    # Fetch the job ensuring it belongs to logged-in employer
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = job.jobapplication_set.all()  # all applications for this job

    if request.method == 'POST':
        action = request.POST.get('action')
        applicant_id = request.POST.get('applicant_id')
        
        if action == 'accept' and applicant_id:
            application = applications.get(applicant__id=applicant_id)
            application.status = 'accepted'
            application.save()
            messages.success(request, f"{application.applicant.user.username} has been accepted.")
        
        elif action == 'message' and applicant_id:
            messages.info(request, "Messaging feature is not yet implemented.")

        return redirect('jobs:employer_job_detail', job_id=job_id)

    return render(request, 'jobs/employer_job_detail.html', {
        'job': job,
        'applications': applications,
    })
@login_required
def login_redirect(request):
    profile = getattr(request.user, 'userprofile', None)
    if not profile:
        messages.error(request, "User profile not found.")
        return redirect('account_logout')  # or a safe page
    
    if profile.is_employer:
        return redirect('users:employer_dashboard')
    else:
        return redirect('users:profile')