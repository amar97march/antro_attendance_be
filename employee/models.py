from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.utils import timezone
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import datetime


class CustomUserManager(BaseUserManager):


    """
    Custom user manager for managing user creation.

    This manager provides methods to create regular users and superusers.
    """

    def create_user(self, email, password=None,hire_date = None ,**extra_fields):

        """
        Create a regular user.

        Args:
            email (str): The email address of the user.
            password (str): The password for the user.
            extra_fields (dict): Additional fields for the user.

        Returns:
            User: The newly created user object.
        """


        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,hire_date = hire_date ,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, hire_date = None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, hire_date = hire_date,**extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    """
    Custom user model representing a user of the application.
    """
    # username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    employee_id = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    hire_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hometown = models.CharField(default= False)
    qualification = models.CharField(default = False)
    hobbies = models.CharField(default = False)
    image = models.ImageField(upload_to='user_images/', height_field=None, width_field=None, max_length=None)
    objects = CustomUserManager()
    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'employee_id', 'department', 'position', 'hire_date','is_staff','is_active','hometown','qualification','hobbies','image']

    def __str__(self):
        return self.email
    
class Attendance(models.Model):

    """
    Model representing attendance records of users.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    check_in = models.DateTimeField(default=datetime.now)
    check_out = models.DateTimeField(null = True, blank = True)
    todays_tasks = models.TextField(null=True, blank=True) 
    tomorrow_tasks = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.date}"
    

class Holiday(models.Model):
    date = models.DateField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



# class Employee(models.Model):
#     employee_id = models.CharField(max_length=20, unique=True)
#     working_hours = models.DecimalField(max_digits=5, decimal_places=2)


class AllowedIP(models.Model):
    ip = models.GenericIPAddressField()
    def __str__(self):
        return self.ip