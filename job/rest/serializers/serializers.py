from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator

from job.models import Job, JobApplication
from job.choices import JobStatusChoices, ApplicationStatusChoices

User = get_user_model()

class JobListSerializer(serializers.ModelSerializer):

    recruiter_name = serializers.CharField(source='recruiter.get_full_name', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    salary_range = serializers.CharField(source='get_salary_range', read_only=True)
    skills_list = serializers.ListField(source='get_skills_list', read_only=True)
    
    class Meta:
        model = Job
        fields = [
            'unique_job_id', 'title', 'recruiter_name', 'location',
            'salary_range', 'job_type', 'experience_level', 'skills_list',
            'deadline', 'is_active', 'created_at'
        ]

class JobDetailSerializer(serializers.ModelSerializer):

    recruiter_name = serializers.CharField(source='recruiter.get_full_name', read_only=True)
    recruiter_email = serializers.EmailField(source='recruiter.email', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_expired = serializers.BooleanField(read_only=True)
    salary_range = serializers.CharField(source='get_salary_range', read_only=True)
    skills_list = serializers.ListField(source='get_skills_list', read_only=True)
    total_applications = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Job
        fields = '__all__'
        read_only_fields = [
            'unique_job_id', 'recruiter', 'total_applications',
            'created_at', 'updated_at'
        ]

class JobCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = [
            'title', 'description', 'requirements', 'location',
            'salary_min', 'salary_max', 'job_type', 'experience_level',
            'skills_required', 'deadline'
        ]
        
    def validate_deadline(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError("Deadline must be in the future.")
        return value
        
    def validate_salary_min(self, value):
        if value and value < 0:
            raise serializers.ValidationError("Salary must be positive.")
        return value
        
    def validate_salary_max(self, value):
        if value and value < 0:
            raise serializers.ValidationError("Salary must be positive.")
        return value
        
    def validate(self, data):
        if data.get('salary_min') and data.get('salary_max'):
            if data['salary_min'] > data['salary_max']:
                raise serializers.ValidationError(
                    "Minimum salary cannot be greater than maximum salary."
                )
        return data

class JobApplicationSerializer(serializers.ModelSerializer):

    job_title = serializers.CharField(source='job.title', read_only=True)
    candidate_name = serializers.CharField(source='candidate.get_full_name', read_only=True)
    recruiter_name = serializers.CharField(source='job.recruiter.get_full_name', read_only=True)
    
    class Meta:
        model = JobApplication
        fields = [
            'id', 'job', 'job_title', 'candidate', 'candidate_name',
            'recruiter_name', 'cover_letter', 'resume', 'application_status',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'candidate', 'application_status', 'created_at', 'updated_at'
        ]
        
    def validate(self, data):
        job = data.get('job') or self.instance.job if self.instance else None
        
        if not job:
            raise serializers.ValidationError("Job is required.")
            
        if not job.is_active:
            raise serializers.ValidationError("This job is no longer accepting applications.")
            
        candidate = self.context['request'].user
        if JobApplication.objects.filter(job=job, candidate=candidate).exists():
            raise serializers.ValidationError("You have already applied to this job.")
            
        return data

class JobApplicationStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobApplication
        fields = ['application_status']
        
    def validate_application_status(self, value):
        if value not in ApplicationStatusChoices.values:
            raise serializers.ValidationError("Invalid application status.")
        return value

class RecruiterDashboardSerializer(serializers.Serializer):

    total_published_jobs = serializers.IntegerField()
    total_closed_jobs = serializers.IntegerField()
    total_candidate_applications = serializers.IntegerField()
    total_candidates_hired = serializers.IntegerField()
    total_candidates_rejected = serializers.IntegerField()