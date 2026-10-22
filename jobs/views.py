from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator

from .models import Job, Application
from .forms import JobForm, ApplicationForm


def home_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    recent_jobs = Job.objects.all().order_by('-created_at')[:6]
    total_jobs = Job.objects.count()

    user_applied_count = 0
    user_applied_job_ids = []
    if request.user.role == 'seeker':
        user_applications = Application.objects.filter(seeker=request.user)
        user_applied_count = user_applications.count()
        user_applied_job_ids = list(user_applications.values_list('job_id', flat=True))

    user_posted_count = 0
    if request.user.role == 'recruiter':
        user_posted_count = Job.objects.filter(recruiter=request.user).count()

    return render(request, 'home.html', {
        'recent_jobs': recent_jobs,
        'total_jobs': total_jobs,
        'user_applied_count': user_applied_count,
        'user_applied_job_ids': user_applied_job_ids,
        'user_posted_count': user_posted_count,
    })



def job_list(request):
    query = request.GET.get('q', '').strip()
    job_type = request.GET.get('job_type', '').strip()

    jobs_qs = Job.objects.all().order_by('-created_at')

    if query:
        jobs_qs = jobs_qs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query) |
            Q(company_name__icontains=query)
        )

    if job_type:
        jobs_qs = jobs_qs.filter(job_type=job_type)

    user_applied_job_ids = []
    if request.user.is_authenticated and request.user.role == 'seeker':
        user_applied_job_ids = list(
            Application.objects.filter(seeker=request.user).values_list('job_id', flat=True)
        )

    paginator = Paginator(jobs_qs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'job_list.html', {
        'jobs': page_obj,
        'page_obj': page_obj,
        'total_count': jobs_qs.count(),
        'query': query,
        'selected_job_type': job_type,
        'user_applied_job_ids': user_applied_job_ids,
        'job_type_choices': Job.JOB_TYPE_CHOICES,
    })


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    has_applied = False
    if request.user.is_authenticated and request.user.role == 'seeker':
        has_applied = Application.objects.filter(job=job, seeker=request.user).exists()

    return render(request, 'job_detail.html', {
        'job': job,
        'has_applied': has_applied,
    })


@login_required
def post_job(request):
    if request.user.role != 'recruiter':
        messages.warning(request, "Only recruiters can post new jobs.")
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, f"Job '{job.title}' posted successfully!")
            return redirect('job_list')
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        form = JobForm()

    return render(request, 'post_job.html', {'form': form})


@login_required
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.user.role != 'seeker':
        messages.warning(request, "Only job seekers can apply for jobs.")
        return redirect('job_list')

    already_applied = Application.objects.filter(
        job=job,
        seeker=request.user
    ).exists()

    if already_applied:
        messages.info(request, "You have already applied for this job.")
        return redirect('job_list')

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.seeker = request.user
            application.save()
            messages.success(request, f"Your application for '{job.title}' was submitted successfully!")
            return redirect('job_list')
        else:
            messages.error(request, "There was a problem with your application submission.")
    else:
        form = ApplicationForm()

    return render(request, 'apply_job.html', {'job': job, 'form': form})


@login_required
def my_applications(request):
    if request.user.role != 'seeker':
        messages.warning(request, "Only job seekers can view their applied jobs.")
        return redirect('home')

    applications = Application.objects.filter(seeker=request.user).select_related('job', 'job__recruiter').order_by('-applied_at')
    return render(request, 'my_applications.html', {'applications': applications})


@login_required
def my_jobs(request):
    if request.user.role != 'recruiter':
        messages.warning(request, "Only recruiters have access to posted jobs management.")
        return redirect('home')

    jobs = Job.objects.filter(recruiter=request.user).annotate(applicant_count=Count('applications')).order_by('-created_at')
    return render(request, 'my_jobs.html', {'jobs': jobs})


@login_required
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)
    applications = Application.objects.filter(job=job).select_related('seeker').order_by('-applied_at')

    status_filter = request.GET.get('status', '').strip()
    if status_filter in ['applied', 'shortlisted', 'rejected']:
        applications = applications.filter(status=status_filter)

    return render(request, 'job_applicants.html', {
        'job': job,
        'applications': applications,
        'selected_status': status_filter,
        'status_choices': Application.STATUS_CHOICES,
        'total_applicants': Application.objects.filter(job=job).count(),
    })


@login_required
def update_application_status(request, app_id, status):
    application = get_object_or_404(Application, id=app_id, job__recruiter=request.user)
    valid_statuses = dict(Application.STATUS_CHOICES).keys()

    if status in valid_statuses:
        application.status = status
        application.save()
        messages.success(request, f"Updated {application.seeker.username}'s application status to '{application.get_status_display()}'.")
    else:
        messages.error(request, "Invalid status choice.")

    return redirect('job_applicants', job_id=application.job.id)


@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"Job '{job.title}' was successfully updated.")
            return redirect('my_jobs')
        else:
            messages.error(request, "Please correct the form errors.")
    else:
        form = JobForm(instance=job)

    return render(request, 'edit_job.html', {'form': form, 'job': job})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, recruiter=request.user)

    if request.method == 'POST':
        title = job.title
        job.delete()
        messages.success(request, f"Job '{title}' has been successfully deleted.")
        return redirect('my_jobs')

    return render(request, 'delete_job.html', {'job': job})




