from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/post/', views.post_job, name='post_job'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('jobs/apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('jobs/my-applications/', views.my_applications, name='my_applications'),
    path('jobs/my-jobs/', views.my_jobs, name='my_jobs'),
    path('jobs/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    path('jobs/application/<int:app_id>/status/<str:status>/', views.update_application_status, name='update_application_status'),
    path('jobs/<int:job_id>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:job_id>/delete/', views.delete_job, name='delete_job'),
]

