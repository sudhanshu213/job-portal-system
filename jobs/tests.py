from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from accounts.models import User
from .models import Job, Application

class JobPortalTestCase(TestCase):
    def setUp(self):
        self.recruiter = User.objects.create_user(
            username='recruiter1',
            password='password123',
            role='recruiter'
        )
        self.seeker = User.objects.create_user(
            username='seeker1',
            password='password123',
            role='seeker'
        )
        self.job = Job.objects.create(
            recruiter=self.recruiter,
            title='Python Developer',
            company_name='Tech Corp',
            location='Remote',
            salary='₹10 LPA',
            job_type='full-time',
            description='We are hiring a Python developer.'
        )

    def test_home_page_unauthenticated_redirects_to_login(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login'))

    def test_home_page_authenticated(self):
        self.client.login(username='seeker1', password='password123')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Developer')


    def test_job_list_and_search(self):
        response = self.client.get(reverse('job_list'), {'q': 'Python'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Developer')

        response_empty = self.client.get(reverse('job_list'), {'q': 'NonExistentTitleXYZ'})
        self.assertEqual(response_empty.status_code, 200)
        self.assertContains(response_empty, 'No matching job vacancies found')

    def test_job_list_pagination(self):
        # Create 7 more jobs (total 8 jobs, default page size is 6)
        for i in range(7):
            Job.objects.create(
                recruiter=self.recruiter,
                title=f'Job Batch {i}',
                company_name='Company Batch',
                location='Remote',
                job_type='full-time',
                description='Batch job desc.'
            )

        # Page 1
        resp_p1 = self.client.get(reverse('job_list'))
        self.assertEqual(resp_p1.status_code, 200)
        self.assertEqual(len(resp_p1.context['jobs']), 6)
        self.assertTrue(resp_p1.context['page_obj'].has_next())

        # Page 2
        resp_p2 = self.client.get(reverse('job_list'), {'page': 2})
        self.assertEqual(resp_p2.status_code, 200)
        self.assertEqual(len(resp_p2.context['jobs']), 2)
        self.assertFalse(resp_p2.context['page_obj'].has_next())


    def test_job_detail_page(self):
        response = self.client.get(reverse('job_detail', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Developer')
        self.assertContains(response, 'Tech Corp')

    def test_recruiter_can_post_job(self):
        self.client.login(username='recruiter1', password='password123')
        response = self.client.post(reverse('post_job'), {
            'title': 'Frontend Engineer',
            'company_name': 'Design Inc',
            'location': 'Bangalore',
            'salary': '₹8 LPA',
            'job_type': 'full-time',
            'description': 'React and CSS expertise needed.',
        })
        self.assertRedirects(response, reverse('job_list'))
        self.assertTrue(Job.objects.filter(title='Frontend Engineer').exists())

    def test_seeker_cannot_post_job(self):
        self.client.login(username='seeker1', password='password123')
        response = self.client.post(reverse('post_job'), {
            'title': 'Illegal Job',
            'description': 'Desc',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(Job.objects.filter(title='Illegal Job').exists())

    def test_seeker_can_apply_job(self):
        self.client.login(username='seeker1', password='password123')
        # 60 KB file (between 50 KB and 1 MB)
        valid_file_content = b"a" * (60 * 1024)
        resume = SimpleUploadedFile("resume.pdf", valid_file_content, content_type="application/pdf")
        response = self.client.post(reverse('apply_job', args=[self.job.id]), {
            'resume': resume
        })
        self.assertRedirects(response, reverse('job_list'))
        self.assertTrue(Application.objects.filter(job=self.job, seeker=self.seeker).exists())

    def test_resume_size_validation(self):
        self.client.login(username='seeker1', password='password123')
        # 1. Test file too small (< 50 KB, e.g. 10 KB)
        small_content = b"a" * (10 * 1024)
        small_resume = SimpleUploadedFile("small_resume.pdf", small_content, content_type="application/pdf")
        response_small = self.client.post(reverse('apply_job', args=[self.job.id]), {
            'resume': small_resume
        })
        self.assertEqual(response_small.status_code, 200)
        self.assertContains(response_small, "File size too small. Resume must be at least 50 KB.")

        # 2. Test file too large (> 1 MB, e.g. 1.2 MB)
        large_content = b"a" * int(1.2 * 1024 * 1024)
        large_resume = SimpleUploadedFile("large_resume.pdf", large_content, content_type="application/pdf")
        response_large = self.client.post(reverse('apply_job', args=[self.job.id]), {
            'resume': large_resume
        })
        self.assertEqual(response_large.status_code, 200)
        self.assertContains(response_large, "File size too large. Resume must be between 50 KB and 1 MB.")

    def test_duplicate_application_prevented(self):
        self.client.login(username='seeker1', password='password123')
        valid_file_content = b"a" * (60 * 1024)
        resume = SimpleUploadedFile("resume.pdf", valid_file_content, content_type="application/pdf")
        self.client.post(reverse('apply_job', args=[self.job.id]), {'resume': resume})

        # Try to apply again
        resume2 = SimpleUploadedFile("resume2.pdf", valid_file_content, content_type="application/pdf")
        response = self.client.post(reverse('apply_job', args=[self.job.id]), {'resume': resume2})
        self.assertRedirects(response, reverse('job_list'))
        self.assertEqual(Application.objects.filter(job=self.job, seeker=self.seeker).count(), 1)

    def test_seeker_my_applications_page(self):
        self.client.login(username='seeker1', password='password123')
        valid_file_content = b"a" * (60 * 1024)
        resume = SimpleUploadedFile("resume.pdf", valid_file_content, content_type="application/pdf")
        self.client.post(reverse('apply_job', args=[self.job.id]), {'resume': resume})

        response = self.client.get(reverse('my_applications'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Developer')
        self.assertContains(response, 'Tech Corp')

    def test_recruiter_blocked_from_my_applications(self):
        self.client.login(username='recruiter1', password='password123')
        response = self.client.get(reverse('my_applications'))
        self.assertRedirects(response, reverse('home'))

    def test_recruiter_my_jobs_page(self):
        self.client.login(username='recruiter1', password='password123')
        response = self.client.get(reverse('my_jobs'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Python Developer')

    def test_seeker_blocked_from_my_jobs(self):
        self.client.login(username='seeker1', password='password123')
        response = self.client.get(reverse('my_jobs'))
        self.assertRedirects(response, reverse('home'))

    def test_recruiter_view_and_update_applicant_status(self):
        # Create an application
        valid_file_content = b"a" * (60 * 1024)
        resume = SimpleUploadedFile("resume.pdf", valid_file_content, content_type="application/pdf")
        app = Application.objects.create(job=self.job, seeker=self.seeker, resume=resume, status='applied')

        # Recruiter views applicants
        self.client.login(username='recruiter1', password='password123')
        response = self.client.get(reverse('job_applicants', args=[self.job.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'seeker1')

        # Recruiter updates status to shortlisted
        update_resp = self.client.get(reverse('update_application_status', args=[app.id, 'shortlisted']))
        self.assertRedirects(update_resp, reverse('job_applicants', args=[self.job.id]))
        app.refresh_from_db()
        self.assertEqual(app.status, 'shortlisted')

    def test_recruiter_edit_and_delete_job(self):
        self.client.login(username='recruiter1', password='password123')
        # Edit Job
        edit_resp = self.client.post(reverse('edit_job', args=[self.job.id]), {
            'title': 'Senior Python Developer',
            'company_name': 'Tech Corp Global',
            'location': 'Remote',
            'salary': '₹15 LPA',
            'job_type': 'full-time',
            'description': 'Updated description.',
        })
        self.assertRedirects(edit_resp, reverse('my_jobs'))
        self.job.refresh_from_db()
        self.assertEqual(self.job.title, 'Senior Python Developer')

        # Delete Job
        del_resp = self.client.post(reverse('delete_job', args=[self.job.id]))
        self.assertRedirects(del_resp, reverse('my_jobs'))
        self.assertFalse(Job.objects.filter(id=self.job.id).exists())


