from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, MaxLengthValidator,RegexValidator
from django.utils import timezone
from django.core.exceptions import ValidationError
# Create your models here.

class Specialty(models.Model):
    name = models.CharField(max_length=50)
    class Meta:
        verbose_name="Specialty"
        verbose_name_plural = "Specialties"
    def __str__(self):
        return self.name


class User(AbstractUser):
    pass
def birth_date_validator(date):
    if date>= timezone.localdate():
        raise ValidationError('la date de naissance doit etre enterieure de la date d ajourd hui.')

class Doctor(User):
    license_number = models.CharField(max_length=6, unique=True, validators=[MinLengthValidator(6), MaxLengthValidator(6)])
    phone = models.CharField(max_length=8, unique=True, validators=[ RegexValidator(r'^\d{8}$', 'Phone number must be 8 digits.')])
    specialities = models.ManyToManyField(Specialty, related_name="doctors")
    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
    def __str__(self):
        return f" DR. {self.first_name} {self.last_name} "
class Patient(User):
    national_id= models.CharField(max_length=8, unique=True , validators=[MinLengthValidator(8), MaxLengthValidator(8)])
    phone = models.CharField(max_length=8, unique=True, validators=[ RegexValidator(r'^\d{8}$', 'Phone number must be 8 digits.')])
    birth_date = models.DateField(blank=True , validators=[birth_date_validator])
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
    def __str__(self):
        return f" {self.first_name} {self.last_name} "






