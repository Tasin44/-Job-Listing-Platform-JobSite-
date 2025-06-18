from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe

from shared.base_admin import BaseModelAdmin
from job.models import Job, JobApplication


@admin.register(Job)
class JobAdmin(BaseModelAdmin):

    model = Job
    list_display = [
        'unique_job_id', 'title', 'recruiter_name', 'location',
        'job_status', 'total_applications', 'deadline_display', 'created_at'
    ]
    list_filter = [
        'job_status', 'job_type', 'experience_level', 
        'created_at', 'deadline'
    ]
    search_fields = [
        'unique_job_id', 'title', 'location', 
        'recruiter__first_name', 'recruiter__last_name', 'recruiter__email'
    ]
    readonly_fields = BaseModelAdmin.readonly_fields + [
        'unique_job_id', 'total_applications'
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('unique_job_id', 'title', 'recruiter', 'job_status')
        }),
        ('Job Details', {
            'fields': (
                'description', 'requirements', 'location', 
                'job_type', 'experience_level', 'skills_required'
            )
        }),
        ('Compensation', {
            'fields': ('salary_min', 'salary_max')
        }),
        ('Timeline', {
            'fields': ('deadline',)
        }),
        ('Statistics', {
            'fields': ('total_applications',),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('uid', 'created_at', 'updated_at', 'status'),
            'classes': ('collapse',)
        })
    )
    
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    def recruiter_name(self, obj):
        """Display recruiter name with link to user admin"""
        if obj.recruiter:
            url = reverse('admin:core_user_change', args=[obj.recruiter.pk])
            return format_html(
                '<a href="{}">{}</a>',
                url, obj.recruiter.get_full_name()
            )
        return '-'
    recruiter_name.short_description = 'Recruiter'
    recruiter_name.admin_order_field = 'recruiter__first_name'

    def deadline_display(self, obj):

        from django.utils import timezone
        if obj.deadline:
            if obj.deadline < timezone.now():
                color = 'red'
                status = 'Expired'
            elif (obj.deadline - timezone.now()).days <= 7:
                color = 'orange'
                status = 'Expiring Soon'
            else:
                color = 'green'
                status = 'Active'
            
            return format_html(
                '<span style="color: {};">{} ({})</span>',
                color, obj.deadline.strftime('%Y-%m-%d %H:%M'), status
            )
        return '-'
    deadline_display.short_description = 'Deadline'
    deadline_display.admin_order_field = 'deadline'

    def get_queryset(self, request):

        return super().get_queryset(request).select_related('recruiter')


@admin.register(JobApplication)
class JobApplicationAdmin(BaseModelAdmin):

    model = JobApplication
    list_display = [
        'application_id', 'candidate_name', 'job_title',
        'application_status_display', 'applied_date', 'recruiter_name'
    ]
    list_filter = [
        'application_status', 'created_at',
        'job__job_status', 'job__recruiter'
    ]
    search_fields = [
        'candidate__first_name', 'candidate__last_name', 'candidate__email',
        'job__title', 'job__unique_job_id'
    ]
    readonly_fields = BaseModelAdmin.readonly_fields + [
        'application_id'
    ]
    
    fieldsets = (
        ('Application Information', {
            'fields': ('job', 'candidate', 'application_status')
        }),
        ('Application Details', {
            'fields': ('cover_letter', 'resume')
        }),
        ('Recruiter Section', {
            'fields': ('recruiter_notes', 'interview_scheduled_at')
        }),
        ('System Fields', {
            'fields': ('uid', 'created_at', 'updated_at', 'status'),
            'classes': ('collapse',)
        })
    )
    
    list_per_page = 25
    date_hierarchy = 'created_at'
    ordering = ['-created_at']

    def application_id(self, obj):
        """Display application ID"""
        return str(obj.uid)[:8] + '...'
    application_id.short_description = 'Application ID'

    def candidate_name(self, obj):
        """Display candidate name with link"""
        if obj.candidate:
            url = reverse('admin:core_user_change', args=[obj.candidate.pk])
            return format_html(
                '<a href="{}">{}</a>',
                url, obj.candidate.get_full_name()
            )
        return '-'
    candidate_name.short_description = 'Candidate'
    candidate_name.admin_order_field = 'candidate__first_name'

    def job_title(self, obj):
        """Display job title with link"""
        if obj.job:
            url = reverse('admin:jobs_job_change', args=[obj.job.pk])
            return format_html(
                '<a href="{}">{}</a>',
                url, obj.job.title
            )
        return '-'
    job_title.short_description = 'Job'
    job_title.admin_order_field = 'job__title'

    def application_status_display(self, obj):
        """Display application status with color coding"""
        colors = {
            'PENDING': 'orange',
            'REVIEWING': 'blue',
            'SHORTLISTED': 'purple',
            'INTERVIEW_SCHEDULED': 'teal',
            'ACCEPTED': 'green',
            'REJECTED': 'red',
            'WITHDRAWN': 'gray'
        }
        color = colors.get(obj.application_status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.get_application_status_display()
        )
    application_status_display.short_description = 'Status'
    application_status_display.admin_order_field = 'application_status'

    def applied_date(self, obj):
        """Display application date"""
        return obj.created_at.strftime('%Y-%m-%d %H:%M')
    applied_date.short_description = 'Applied Date'
    applied_date.admin_order_field = 'created_at'

    def recruiter_name(self, obj):
        """Display recruiter name"""
        if obj.job and obj.job.recruiter:
            return obj.job.recruiter.get_full_name()
        return '-'
    recruiter_name.short_description = 'Recruiter'

    def get_queryset(self, request):
        """Optimize queries with select_related"""
        return super().get_queryset(request).select_related(
            'candidate', 'job', 'job__recruiter'
        )
