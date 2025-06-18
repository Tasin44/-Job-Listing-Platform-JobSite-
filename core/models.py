from django.contrib.auth.base_user import  AbstractBaseUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from core.choices import GenderChoices,UserRoleChoices
from core.managers import UserManager
from shared.base_model import BaseModel


class User(AbstractBaseUser, PermissionsMixin, BaseModel):
    username = models.CharField(max_length=50, unique=True, db_index=True)
    password = models.CharField(max_length=128, blank=True)
    new_password = models.CharField(max_length=128, blank=True)
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=15, blank=True)

    role = models.CharField(
        max_length=20, 
        choices=UserRoleChoices.choices, 
        default=UserRoleChoices.CANDIDATE,
        help_text="User role determines access permissions"
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    

    is_email_verified = models.BooleanField(default=False)


    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"


    def __str__(self):
        return f"uid:{self.uid} {self.email}"
 
    def get_full_name(self):
        """Return the full name of the user"""
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):

        return self.first_name

    def save(self, *args, **kwargs):

        if not self.pk:

            if self.password:
                self.password = make_password(self.password)

            self.username = self.email if not self.username else self.username


        if self.new_password:
            self.password = make_password(self.new_password)
            self.new_password = ""

        super().save(*args, **kwargs)

    @property
    def is_recruiter(self):

        return self.role == UserRoleChoices.RECRUITER

    @property
    def is_candidate(self):

        return self.role == UserRoleChoices.CANDIDATE

class UserProfile(BaseModel):

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="profile"
    )
    photo = models.ImageField(
        upload_to="profile_pictures/", 
        blank=True,
        help_text="Profile picture"
    )
    bio = models.TextField(
        blank=True,
        help_text="Brief description about the user"
    )
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=20, 
        choices=GenderChoices.choices, 
        default=GenderChoices.NOT_SET
    )
    

    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    

    resume = models.FileField(
        upload_to="resumes/", 
        blank=True,
        help_text="Upload resume/CV"
    )
    skills = models.TextField(
        blank=True,
        help_text="Comma-separated list of skills"
    )
    experience_years = models.PositiveIntegerField(
        null=True, 
        blank=True,
        help_text="Years of experience"
    )

    class Meta:
        db_table = "user_profiles"
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"

    def get_skills_list(self):

        if self.skills:
            return [skill.strip() for skill in self.skills.split(',')]
        return []
    




