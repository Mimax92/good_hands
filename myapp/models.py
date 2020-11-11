
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model



class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()



class Category(models.Model):
    name =  models.CharField(max_length=200)
    name_pl = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Instytution(models.Model):
    TYPE = {
        (0, 'fundacja'),
        (1, 'organizacja pozarządowa'),
        (2, 'zbiórka lokalna'),
        (3, 'domyślnie fundacja'),
    }
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=600)
    type = models.PositiveSmallIntegerField(choices=TYPE)
    categories = models.ManyToManyField(Category)
    def __str__(self):
        return self.name

class Donation(models.Model):
    quantity = models.PositiveSmallIntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Instytution, related_name="instytution", on_delete = models.CASCADE)
    user = models.ForeignKey(get_user_model(), related_name="User", on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=9, blank=True)
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6)
    pick_up_date = models.DateField(auto_now_add=False)
    pick_up_time = models.TimeField(auto_now=False, auto_now_add=False)
    pick_up_comment = models.CharField(max_length=250, null=True)
    is_taken = models.BooleanField(default=False)
