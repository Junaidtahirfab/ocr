from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom user manager for creating users and superusers.
    """
    def create_user(self, email, password=None):
        """
        Create a new user with the given email and password.
        """
        if not email:
            raise ValueError("User must have an email address")

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.is_active = True  # Set is_active to True by default
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None):
        """
        Create a new superuser with the given email and password.
        """
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self.db)
        return user

class CreatedUpdatedMixin(models.Model):
    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Company(models.Model):
    name           = models.CharField(max_length=255, blank=True, null=True)
    category       = models.CharField(max_length=100, blank=True, null=True)
    address_line_1 = models.CharField(max_length=255, blank=True, null=True)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    city           = models.CharField(max_length=100, blank=True, null=True)
    zip_code       = models.CharField(max_length=20,  blank=True, null=True)
    country        = models.CharField(max_length=100, blank=True, null=True)
    state          = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name
class User(CreatedUpdatedMixin,AbstractBaseUser):
    email        = models.EmailField(unique=True)
    first_name   = models.CharField(max_length=100, blank=True, null=True)
    last_name    = models.CharField(max_length=100, blank=True, null=True)
    phone        = models.CharField(max_length=15,  blank=True, null=True)
    password     = models.CharField(max_length=128, blank=True, null=True)  # Store hashed password, not plain text
    city         = models.CharField(max_length=100, blank=True, null=True)
    zip_code     = models.CharField(max_length=20,  blank=True, null=True)
    country      = models.CharField(max_length=100, blank=True, null=True)
    state        = models.CharField(max_length=100, blank=True, null=True)
    address_1    = models.CharField(max_length=255, blank=True, null=True)
    address_2    = models.CharField(max_length=255, blank=True, null=True)
    gender       = models.CharField(max_length=25,  blank=True, null=True)
    date_of_birth= models.DateField(null=True,blank=True)
    is_admin     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_verfied   = models.BooleanField(default=False)
    company      = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True) 
    role         = models.ForeignKey(Role,       on_delete=models.CASCADE, blank=True, null=True)
    
    
    USERNAME_FIELD   = "email"
    objects= UserManager()
    
    def __str__ (self):
        return self.email

    def has_perm(self, perm , obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True

class OtpVerify(CreatedUpdatedMixin):
    email  = models.EmailField(unique=True,null=True,blank=True)
    user   = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    otp    = models.CharField(max_length=6)

    def __str__(self):
        if self.user:
            return self.user.email
        else:
            return self.email
    
    
    
