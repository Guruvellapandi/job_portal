from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('delete_account/', views.delete_account, name='delete_account'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/manage/', views.job_manage, name='job_manage'),
    path('jobs/manage_users/', views.manage_users, name='manage_users'),
    path('jobs/edit_user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('jobs/apply/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('jobs/applied/', views.applied_jobs, name='applied_jobs'),
]
