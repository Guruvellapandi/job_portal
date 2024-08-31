from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)  # Profile picture field
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)  # Resume field
    bio = models.TextField(blank=True, null=True)  # Bio field
    linkedin = models.URLField(max_length=200, blank=True, null=True)  # LinkedIn profile field

    def __str__(self):
        return self.user.username

class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('INT', 'Internship'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=3, choices=JOB_TYPE_CHOICES)
    domain = models.CharField(max_length=100)
    posted_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title


from .models import Job

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    applied_on = models.DateTimeField(auto_now_add=True)  # Ensure this field is present

    def __str__(self):
        return f'{self.user.username} applied for {self.job.title}'
