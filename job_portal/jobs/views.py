from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .forms import UserRegistrationForm, UserProfileForm, JobForm, JobSearchForm
from .models import Job, UserProfile, JobApplication
from django.contrib import messages
from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    user = request.user
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=user)
        user_profile.save()

    if request.method == 'POST':
        if 'remove_profile_picture' in request.POST:
            user_profile.profile_picture.delete()
        elif 'remove_resume' in request.POST:
            user_profile.resume.delete()
        else:
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')
    profile_form = UserProfileForm(instance=user_profile)
    return render(request, 'profile.html', {'profile_form': profile_form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        logout(request)
        return redirect(reverse('login'))
    return render(request, 'delete_account.html')

def job_list(request):
    jobs = Job.objects.all()
    if 'job_type' in request.GET:
        jobs = jobs.filter(job_type=request.GET['job_type'])
    if 'domain' in request.GET:
        jobs = jobs.filter(domain=request.GET['domain'])
    return render(request, 'job_list.html', {'jobs': jobs})

@login_required
def job_manage(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    if request.method == 'POST':
        if 'delete_job' in request.POST:
            job_id = request.POST.get('job_id')
            job = get_object_or_404(Job, id=job_id)
            job.delete()
            return redirect('job_manage')
        else:
            job_form = JobForm(request.POST)
            if job_form.is_valid():
                job_form.save()
                return redirect('job_manage')
    else:
        job_form = JobForm()

    jobs = Job.objects.all()
    return render(request, 'job_manage.html', {'job_form': job_form, 'jobs': jobs})

@login_required
def apply_for_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    
    # Check if the user has already applied for this job
    if JobApplication.objects.filter(user=request.user, job=job).exists():
        messages.info(request, f'You have already applied for the job: {job.title}')
    else:
        # Create a new job application
        JobApplication.objects.create(user=request.user, job=job)
        messages.success(request, f'You have successfully applied for the job: {job.title}')
    
    return redirect('applied_jobs')  # Redirect to the applied jobs page

def home(request):
    return render(request, 'home.html')


def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Login the user
            login(request, user)
            return redirect('profile')
        else:
            # Add an error message if authentication fails
            messages.error(request, 'Invalid username or password.')
    
    # Render the login form
    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def manage_users(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")

    if request.method == 'POST':
        if 'add_user' in request.POST:
            add_user_form = UserRegistrationForm(request.POST)
            if add_user_form.is_valid():
                # Save the new user
                add_user_form.save()
                return redirect('manage_users')
            else:
                # Print form errors for debugging
                print("Add user form errors:", add_user_form.errors)
        
        elif 'delete_user' in request.POST:
            user_id = request.POST.get('user_id')
            user = get_object_or_404(User, id=user_id)
            user.delete()
            return redirect('manage_users')

    users = User.objects.all()
    add_user_form = UserRegistrationForm()
    return render(request, 'manage_users.html', {
        'users': users,
        'add_user_form': add_user_form
    })

@login_required
def edit_user(request, user_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to access this page.")
    
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
    else:
        form = UserRegistrationForm(instance=user)
    
    return render(request, 'edit_user.html', {'form': form})

@login_required
def applied_jobs(request):
    user = request.user
    applied_jobs = JobApplication.objects.filter(user=user)

    if request.method == 'GET':
        form = JobSearchForm(request.GET)
        if form.is_valid():
            applied_jobs = form.filter_jobs(applied_jobs)
    else:
        form = JobSearchForm()

    return render(request, 'applied_jobs.html', {
        'applied_jobs': applied_jobs,
        'form': form
    })
