from django.db import models


class GenderChoices(models.TextChoices):
    MALE = "MALE", "Male"
    FEMALE = "FEMALE", "Female"
    OTHER = "OTHER", "Other"
    NOT_SPECIFIED = "NOT_SPECIFIED", "Not Specified"
    NOT_SET = "NOT_SET", "Not Set"

class UserRoleChoices(models.TextChoices):
    """User role choices for role-based access control"""
    RECRUITER = "RECRUITER", "Recruiter"
    CANDIDATE = "CANDIDATE", "Candidate"


class StatusChoices(models.TextChoices):
    """General status choices"""
    ACTIVE = "ACTIVE", "Active"
    INACTIVE = "INACTIVE", "Inactive"
    PENDING = "PENDING", "Pending"
    SUSPENDED = "SUSPENDED", "Suspended"
