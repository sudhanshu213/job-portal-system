import os
from django import forms
from django.core.exceptions import ValidationError
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title",
            "company_name",
            "location",
            "salary",
            "job_type",
            "description",
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Senior Python Developer'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Google, Infosys, Startup'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Bangalore / Remote'}),
            'salary': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. ₹8-12 LPA or Negotiable'}),
            'job_type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Job responsibilities, requirements, qualifications...'}),
        }


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']
        widgets = {
            'resume': forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.doc,.docx'}),
        }

    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if not resume:
            raise ValidationError("Please select a resume file.")

        ext = os.path.splitext(resume.name)[1].lower()
        valid_extensions = ['.pdf', '.doc', '.docx']
        if ext not in valid_extensions:
            raise ValidationError("Invalid file format. Please upload a PDF, DOC, or DOCX file.")

        min_size = 50 * 1024       # 50 KB
        max_size = 1 * 1024 * 1024 # 1 MB

        if resume.size < min_size:
            raise ValidationError("File size too small. Resume must be at least 50 KB.")

        if resume.size > max_size:
            raise ValidationError("File size too large. Resume must be between 50 KB and 1 MB.")

        return resume

