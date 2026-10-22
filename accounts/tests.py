from django.test import TestCase
from django.urls import reverse
from .models import User

class AccountsTestCase(TestCase):
    def test_user_registration_seeker(self):
        response = self.client.post(reverse('register'), {
            'username': 'john_seeker',
            'email': 'john@example.com',
            'role': 'seeker',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('login'))
        user = User.objects.get(username='john_seeker')
        self.assertEqual(user.role, 'seeker')
        self.assertTrue(user.is_seeker)
        self.assertFalse(user.is_recruiter)

    def test_user_registration_recruiter(self):
        response = self.client.post(reverse('register'), {
            'username': 'jane_recruiter',
            'email': 'jane@example.com',
            'role': 'recruiter',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })
        self.assertRedirects(response, reverse('login'))
        user = User.objects.get(username='jane_recruiter')
        self.assertEqual(user.role, 'recruiter')
        self.assertTrue(user.is_recruiter)

    def test_profile_view_and_update(self):
        user = User.objects.create_user(username='profileuser', password='password123', role='seeker')
        self.client.login(username='profileuser', password='password123')

        # Get profile page
        get_resp = self.client.get(reverse('profile'))
        self.assertEqual(get_resp.status_code, 200)
        self.assertContains(get_resp, 'Account & Profile Settings')

        # Update profile
        post_resp = self.client.post(reverse('profile'), {
            'first_name': 'Profile',
            'last_name': 'Tester',
            'email': 'profile@example.com',
            'phone': '+91 9999999999',
            'location': 'Mumbai',
            'bio': 'Passionate software developer.',
            'skills': 'Python, Django, PostgreSQL',
            'experience_years': 3,
            'education': 'B.Tech CS',
        })
        self.assertRedirects(post_resp, reverse('profile'))
        user.refresh_from_db()
        self.assertEqual(user.first_name, 'Profile')
        self.assertEqual(user.profile.phone, '+91 9999999999')
        self.assertEqual(user.profile.skills, 'Python, Django, PostgreSQL')

