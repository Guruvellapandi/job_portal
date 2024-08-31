# job_portal/urls.py
from django.contrib import admin
from django.urls import path, include
from jobs import views as job_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('jobs/', include('jobs.urls')),
    path('', job_views.custom_login, name='custom_login'),  # Root URL points to the home view
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # ... other paths
]
