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
import os
# 🟢 User Profile View
@login_required
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

# 🟢 Employer Signup View
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

            # Create user
            user = User.objects.create_user(username=username, password=password, email=email)

            # ✅ **Just update the existing profile instead of creating a new one:**
            user.userprofile.is_employer = True
            user.userprofile.company_name = company_name
            user.userprofile.save()

            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')

            messages.success(request, "Employer account created successfully!")
            return redirect('users:employer_dashboard')
    else:
        form = EmployerSignupForm()
    return render(request, 'users/employer_signup.html', {'form': form})


# 🟢 Employer Dashboard View
@login_required
def employer_dashboard(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if not profile.is_employer:
            messages.error(request, "Access denied. Only employers can access this page.")
            return redirect('users:profile')
    except UserProfile.DoesNotExist:
        messages.error(request, "UserProfile not found.")
        return redirect('users:profile')

    jobs = Job.objects.filter(employer=request.user).annotate(applications_count=Count('jobapplication')).order_by('-created_at')


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

    context = {
        'jobs': page_obj,
        'profile': profile,
    }
    return render(request, 'users/employer_dashboard.html', context)

def employer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user is an employer
            if hasattr(user, 'userprofile') and user.userprofile.is_employer:
                login(request, user)
                return redirect('users:employer_dashboard')  # Redirect to employer dashboard
            else:
                messages.error(request, "This account is not an employer.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'users/employer_login.html')

@login_required
def employer_job_detail(request, job_id):
    # Fetch the job with the given ID, ensure it belongs to the logged-in employer
    job = get_object_or_404(Job, id=job_id, employer=request.user)
    applications = job.jobapplication_set.all()  # Fetch all applications for this job

    if request.method == 'POST':
        action = request.POST.get('action')
        applicant_id = request.POST.get('applicant_id')
        
        if action == 'accept' and applicant_id:
            application = applications.get(applicant__id=applicant_id)
            application.status = 'accepted'
            application.save()
            messages.success(request, f"{application.applicant.username} has been accepted.")
        
        elif action == 'message' and applicant_id:
            # Optional: Redirect to a message page or open a chat
            messages.info(request, "Messaging feature is not yet implemented.")

        return redirect('jobs:employer_job_detail', job_id=job_id)

    return render(request, 'jobs/employer_job_detail.html', {
        'job': job,
        'applications': applications,
    })