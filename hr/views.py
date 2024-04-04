from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from hr.models import JobPost , CandidateApplications , SelectCandidateJob
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import Hr
from .decorators import is_hr, hr_required
from datetime import datetime, timedelta  
from django.core.mail import send_mail

@hr_required
def hrHome(request):
    if is_hr(request.user):
        jobposts = JobPost.objects.filter(user=request.user)
        return render(request, 'hr/hrdash.html', {'jobposts': jobposts})
    else:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('homepage')


def hrCandidateDetails(request,id):
    if JobPost.objects.filter(id=id).exists():
        jobpost = JobPost.objects.get(id=id)
        jobapplys = CandidateApplications.objects.filter(job=jobpost)
        # print(jobapplys)
        selectedCandidate = SelectCandidateJob.objects.filter(job=jobpost)
        print(selectedCandidate)
        return render(request,'hr/candidate.html',{'jobapplys':jobapplys,'jobpost':jobpost,'selectedCandidate':selectedCandidate})
    else:
        return render('hrdash') 


@user_passes_test(is_hr)
def postJobs(request):
    if request.method == 'POST':
        job_title = request.POST.get('job-title')
        address = request.POST.get('address')
        company_name = request.POST.get('company-name')
        salary_low = request.POST.get('salary-low')
        salary_high = request.POST.get('salary-high')
        last_date  = request.POST.get('last-date')

        jobpost = JobPost(user=request.user,title=job_title,address=address,companyName=company_name,salaryLow=salary_low,salaryHigh=salary_high,lastDateToApply=last_date)
        jobpost.save()
        msg = "Job Upload Done.."
        return render(request,'hr/postjob.html',{'msg':msg})
    return render(request,'hr/postjob.html')


@login_required
def acceptApplication(request):
    if request.method == 'POST':
        candidateid = request.POST.get('candidateid')
        jobpostid = request.POST.get('jobpostid') 
        candidate = CandidateApplications.objects.get(id=candidateid) 
        candidate.status = 'accepted'  # Modify the status field
        candidate.save()
        
        # Get the job post and user information
        jobpost = JobPost.objects.get(id=jobpostid)
        user = candidate.user
        
        # Calculate the interview date (today + 3 days) and time (10:00 AM)
        interview_date = datetime.now() + timedelta(days=3)
        interview_time = "10:00 AM"
        
        # Get the HR user's email
        hr_email = request.user.email
        
        # Send email to the user
        send_mail(
            f"Congratulations! Your application for {jobpost.title} has been accepted",
            f"Dear {user.username},\n\n"
            f"We are pleased to inform you that your application for the position of {jobpost.title} has been accepted.\n"
            f"You have been selected for an interview. Please find the details below:\n\n"
            f"Job Title: {jobpost.title}\n"
            f"Interview Date: {interview_date.strftime('%Y-%m-%d')}\n"
            f"Interview Time: {interview_time}\n"
            f"Location: Online\n\n"
            f"We look forward to meeting you!\n\n"
            f"Best regards,\nThe HR Team",
            hr_email,  # Use the HR's email dynamically
            [user.email],  # Send to the user's email
            fail_silently=False,
        )
        
        return redirect('/candidatedetails/' + str(jobpostid) + "/")
    return redirect('hrdash')

@login_required
def rejectApplication(request):
    if request.method == 'POST':
        candidateid = request.POST.get('candidateid')
        jobpostid = request.POST.get('jobpostid') 
        candidate = CandidateApplications.objects.get(id=candidateid) 
        candidate.status = 'rejected'  # Modify the status field to rejected
        candidate.save()
        
        # Get the job post and user information
        jobpost = JobPost.objects.get(id=jobpostid)
        user = candidate.user
        
        # Get the HR user's email
        hr_email = request.user.email
        
        # Send email to the user
        send_mail(
            f"Application Update: Your application for {jobpost.title}",
            f"Dear {user.username},\n\n"
            f"We regret to inform you that your application for the position of {jobpost.title} has been rejected.\n"
            f"We appreciate your interest and wish you the best of luck in your job search.\n\n"
            f"Best regards,\nThe HR Team",
            hr_email,  # Use the HR's email dynamically
            [user.email],  # Send to the user's email
            fail_silently=False,
        )
        
        return redirect('/candidatedetails/' + str(jobpostid) + "/")
    return redirect('hrdash')