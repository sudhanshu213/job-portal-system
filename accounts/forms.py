from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class RegisterForm(UserCreationForm):
    ROLE_CHOICES = (
        ('seeker', 'Job Seeker (Looking for a Job)'),
        ('recruiter', 'Recruiter (Hiring Candidates)'),
    )
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        label="Register As",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Choose a username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'avatar',
            'phone',
            'location',
            'bio',
            'skills',
            'experience_years',
            'education',
            'company_name',
            'company_website',
            'company_about',
        ]
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 9876543210'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City, Country'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Short summary...'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Python, Django, SQL, React'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'education': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. B.Tech in Computer Science'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'company_website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://company.com'}),
            'company_about': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'About company culture...'}),
        }

