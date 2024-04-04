# models.py in candidate

from django.db import models
from hr.models import JobPost , CandidateApplications
from django.contrib.auth.models import User
from django.conf import settings

class MyApplyJobList(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    job = models.ForeignKey(CandidateApplications, on_delete=models.CASCADE)
    dateYouApply = models.DateTimeField(auto_now_add=True)


