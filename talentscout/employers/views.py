from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Applicant
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.models import UserProfile

@login_required
def dashboard(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
        if not profile.is_employer:
            messages.error(request, "You do not have access to the Employer Dashboard.")
            return redirect('users:profile')
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('users:profile')
    
    return render(request, 'employers/dashboard.html')


@login_required
def applicant_list(request):
    applicants = Applicant.objects.filter(job__employer=request.user)
    skill_filter = request.GET.get('skill')
    status_filter = request.GET.get('status')

    if skill_filter:
        applicants = applicants.filter(user__userprofile__skills__icontains=skill_filter)
    if status_filter:
        applicants = applicants.filter(application_status=status_filter)

    return render(request, 'employers/applicant_list.html', {'applicants': applicants})
