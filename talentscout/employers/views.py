from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Applicant
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from users.decorators import employer_required 

@login_required
@employer_required
def dashboard(request):
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
