from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from hr.models import JobPost , CandidateApplications
from candidate.models import MyApplyJobList
from django.core.mail import send_mail
# Create your views here.

@login_required
def candidateHome(request):
    jobpost = JobPost.objects.all()
    return render(request,'candidate/dashboradh.html',{'jobpost':jobpost})

@login_required
def applyJob(request, id):
    if request.method == 'POST':
        # Retrieving form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        college = request.POST.get('college')
        passing_year = request.POST.get('passing_year')
        yearOfExperience = request.POST.get('yearOfExperience')
        resume = request.FILES.get('resume')
        
        # Retrieving the job post object
        job = JobPost.objects.get(id=id)
        
        # Checking if the candidate has already applied for this job
        if CandidateApplications.objects.filter(user=request.user, job=job).exists():
            return redirect('dash')  # Redirecting to dashboard if already applied
        
        job.applyCount=job.applyCount+1
        job.save()
        # Creating and saving a new instance for CandidateApplications model
        candidate_application = CandidateApplications.objects.create(
            user=request.user,
            job=job,
            passingYear=passing_year,
            yearOfExperience=yearOfExperience,
            resume=resume
        )
        
        # Creating and saving a new instance for MyApplyJobList model
        my_apply_job_list = MyApplyJobList.objects.create(
            user=request.user,
            job=candidate_application
        )
        # Send email notification
        subject = 'Confirmation of Job Application'
        message = f"Dear {name},\n\nThank you for applying for the position of '{job.title}' with us. Your application has been received. We will review your application and contact you if you are shortlisted for the next steps in the recruitment process.\n\nBest regards,\nHelping Hands"
        send_mail(subject, message, 'helping.hand.offical.info@gmail.com', [email])
        
        return redirect('dash')  # Redirecting to dashboard after successful application submission
    
    # If request method is not POST, render the application form
    return render(request, 'candidate/apply.html')

@login_required
def myjoblist(request):
    joblist = MyApplyJobList.objects.filter(user=request.user)
    print( joblist)
    return render(request,'candidate/myjoblist.html',{'joblist':joblist})

