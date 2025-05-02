from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    """Manager for CustomUser with email-based authentication"""
    
    def create_user(self, email, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model using email instead of username"""
    
    strava_id = models.IntegerField()
    email = models.EmailField(null=True, unique=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    profile_picture = models.URLField(max_length=500, blank=True, null=True)
    strava_refresh_token = models.CharField(max_length=200, blank=True)
    strava_access_token = models.CharField(max_length=200, blank=True)
    strava_token_expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    
    class Meta:
        constraints = [
            # Ensure either email or strava_id is provided
            models.CheckConstraint(
                check=models.Q(email__isnull=False) | models.Q(strava_id__isnull=False),
                name='either_email_or_strava_required'
            )
        ]

    def __str__(self):
        return self.email
    
class AthleteManager(BaseUserManager):
    def create_user(self, email=None, password=None, strava_id=None, **extra_fields):
        # Require either email or strava_id
        if not email and not strava_id:
            raise ValueError('Either email or Strava ID is required')
           
        # Create a new user instance
        user = self.model(
            email=self.normalize_email(email) if email else None,
            strava_id=strava_id,
            **extra_fields
        )
       
        # Handle password
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
           
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
       
        if not email:
            raise ValueError('Email is required for superusers')
           
        return self.create_user(email=email, password=password, **extra_fields)

