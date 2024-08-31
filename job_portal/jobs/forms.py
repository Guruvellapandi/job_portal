from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, Job
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        }
        help_texts = {
            'username': '',
            'password1': '',
            'password2': '',
        }
        error_messages = {
            'password_mismatch': {
                'message': 'The two password fields must match.',
            },
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

class SimpleLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'placeholder': 'Username'}))

class UserProfileForm(forms.ModelForm):
    remove_profile_picture = forms.BooleanField(required=False, label='Remove profile picture')
    remove_resume = forms.BooleanField(required=False, label='Remove resume')

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'resume', 'bio', 'linkedin']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        if self.cleaned_data.get('remove_profile_picture'):
            user_profile.profile_picture.delete(save=False)
            user_profile.profile_picture = None
        if self.cleaned_data.get('remove_resume'):
            user_profile.resume.delete(save=False)
            user_profile.resume = None
        if commit:
            user_profile.save()
        return user_profile

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'company', 'location', 'job_type', 'domain']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean_title(self):
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError("This field is required.")
        return title

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
        }

class JobSearchForm(forms.Form):
    title = forms.CharField(max_length=100, required=False, label='Job Title')
    company = forms.CharField(max_length=100, required=False, label='Company')

    def filter_jobs(self, queryset):
        if self.cleaned_data['title']:
            queryset = queryset.filter(job__title__icontains=self.cleaned_data['title'])
        if self.cleaned_data['company']:
            queryset = queryset.filter(job__company__icontains=self.cleaned_data['company'])
        return queryset

