from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Job, Application
from .forms import JobForm


def home_view(request):
    return render(request, 'home.html')


@login_required
def post_job(request):
    if request.user.role != 'recruiter':
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)

        if form.is_valid():
            job = form.save(commit=False)
            job.recruiter = request.user
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('job_list')

    else:
        form = JobForm()

    return render(request, 'post_job.html', {'form': form})


def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'job_list.html', {'jobs': jobs})


@login_required
def apply_job(request, job_id):

    job = Job.objects.get(id=job_id)

    if request.user.role != 'seeker':
        return redirect('home')

    already_applied = Application.objects.filter(
        job=job,
        seeker=request.user
    ).exists()

    if already_applied:
        messages.info(request, "You already applied to this job.")
        return redirect('job_list')

    if request.method == 'POST':
        resume = request.FILES.get('resume')

        Application.objects.create(
            job=job,
            seeker=request.user,
            resume=resume
        )

        messages.success(request, "Applied successfully!")
        return redirect('job_list')

    return render(request, 'apply_job.html', {'job': job})


