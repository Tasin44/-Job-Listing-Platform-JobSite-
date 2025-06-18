from django.db import models


class JobStatusChoices(models.TextChoices):
    """Choices for job posting status"""
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    CLOSED = "CLOSED", "Closed"
    CANCELLED = "CANCELLED", "Cancelled"


class ApplicationStatusChoices(models.TextChoices):
    """Choices for job application status"""
    PENDING = "PENDING", "Pending Review"
    REVIEWING = "REVIEWING", "Under Review"
    SHORTLISTED = "SHORTLISTED", "Shortlisted"
    INTERVIEW_SCHEDULED = "INTERVIEW_SCHEDULED", "Interview Scheduled"
    ACCEPTED = "ACCEPTED", "Accepted/Hired"
    REJECTED = "REJECTED", "Rejected"
    WITHDRAWN = "WITHDRAWN", "Withdrawn by Candidate"


class ExperienceLevelChoices(models.TextChoices):
    """Choices for experience level requirements"""
    ENTRY = "ENTRY", "Entry Level"
    JUNIOR = "JUNIOR", "Junior Level"
    MID = "MID", "Mid Level"
    SENIOR = "SENIOR", "Senior Level"
    LEAD = "LEAD", "Lead/Principal Level"
    EXECUTIVE = "EXECUTIVE", "Executive Level"


class JobTypeChoices(models.TextChoices):
    """Choices for job types"""
    FULL_TIME = "FULL_TIME", "Full-time"
    PART_TIME = "PART_TIME", "Part-time"
    CONTRACT = "CONTRACT", "Contract"
    TEMPORARY = "TEMPORARY", "Temporary"
    INTERNSHIP = "INTERNSHIP", "Internship"
    FREELANCE = "FREELANCE", "Freelance"
