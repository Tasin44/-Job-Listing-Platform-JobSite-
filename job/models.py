""" Implement your job related models here. """

import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone

from shared.base_model import BaseModel
from job.choices import JobStatusChoices, ApplicationStatusChoices

User = get_user_model()


class Job(BaseModel):

    unique_job_id = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        help_text="Unique identifier for the job posting"
    )
    

    title = models.CharField(
        max_length=200,
        help_text="Job title"
    )
    description = models.TextField(
        help_text="Detailed job description"
    )
    requirements = models.TextField(
        blank=True,
        help_text="Job requirements and qualifications"
    )
    

    location = models.CharField(
        max_length=200,
        help_text="Job location (city/remote/hybrid)"
    )
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Minimum salary range"
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)],
        help_text="Maximum salary range"
    )
    

    job_type = models.CharField(
        max_length=50,
        default='Full-time',
        help_text="Employment type (Full-time, Part-time, Contract, etc.)"
    )
    experience_level = models.CharField(
        max_length=50,
        default='Mid-level',
        help_text="Required experience level"
    )
    skills_required = models.TextField(
        blank=True,
        help_text="Comma-separated list of required skills"
    )
    

    deadline = models.DateTimeField(
        help_text="Application deadline"
    )
    

    job_status = models.CharField(
        max_length=20,
        choices=JobStatusChoices.choices,
        default=JobStatusChoices.PUBLISHED,
        help_text="Current status of the job posting"
    )
    

    recruiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posted_jobs',
        help_text="Recruiter who posted this job"
    )
    

    total_applications = models.PositiveIntegerField(
        default=0,
        help_text="Total number of applications received"
    )
    
    class Meta:
        db_table = 'jobs'
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['unique_job_id']),
            models.Index(fields=['recruiter', 'job_status']),
            models.Index(fields=['deadline']),
        ]

    def __str__(self):
        return f"{self.unique_job_id} - {self.title}"

    def save(self, *args, **kwargs):

        if not self.unique_job_id:
            self.unique_job_id = self.generate_unique_job_id()
        super().save(*args, **kwargs)

    def generate_unique_job_id(self):

        import random
        import string
        
        prefix = "JOB"
        while True:
            random_part = ''.join(random.choices(string.digits, k=6))
            job_id = f"{prefix}{random_part}"
            if not Job.objects.filter(unique_job_id=job_id).exists():
                return job_id

    @property
    def is_active(self):

        return (
            self.job_status == JobStatusChoices.PUBLISHED and
            self.deadline > timezone.now() and
            self.status == 'ACTIVE'
        )

    @property
    def is_expired(self):

        return self.deadline <= timezone.now()

    def get_skills_list(self):

        if self.skills_required:
            return [skill.strip() for skill in self.skills_required.split(',')]
        return []

    def get_salary_range(self):

        if self.salary_min and self.salary_max:
            return f"${self.salary_min:,.0f} - ${self.salary_max:,.0f}"
        elif self.salary_min:
            return f"From ${self.salary_min:,.0f}"
        elif self.salary_max:
            return f"Up to ${self.salary_max:,.0f}"
        return "Salary not specified"


class JobApplication(BaseModel):

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications',
        help_text="Job being applied to"
    )
    candidate = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_applications',
        help_text="Candidate applying for the job"
    )
    

    cover_letter = models.TextField(
        blank=True,
        help_text="Cover letter from the candidate"
    )
    resume = models.FileField(
        upload_to='application_resumes/',
        blank=True,
        help_text="Resume file uploaded for this application"
    )
    

    application_status = models.CharField(
        max_length=20,
        choices=ApplicationStatusChoices.choices,
        default=ApplicationStatusChoices.PENDING,
        help_text="Current status of the application"
    )
    

    recruiter_notes = models.TextField(
        blank=True,
        help_text="Notes from the recruiter about this application"
    )

    interview_scheduled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Scheduled interview date and time"
    )
    
    class Meta:
        db_table = 'job_applications'
        verbose_name = 'Job Application'
        verbose_name_plural = 'Job Applications'
        ordering = ['-created_at']
        

        unique_together = ['job', 'candidate']
        
        indexes = [
            models.Index(fields=['job', 'application_status']),
            models.Index(fields=['candidate', 'application_status']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.candidate.get_full_name()} applied to {self.job.title}"

    def save(self, *args, **kwargs):

        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:

            self.job.total_applications = self.job.applications.count()
            self.job.save(update_fields=['total_applications'])

    @property
    def is_pending(self):

        return self.application_status == ApplicationStatusChoices.PENDING

    @property
    def is_accepted(self):

        return self.application_status == ApplicationStatusChoices.ACCEPTED

    @property
    def is_rejected(self):

        return self.application_status == ApplicationStatusChoices.REJECTED