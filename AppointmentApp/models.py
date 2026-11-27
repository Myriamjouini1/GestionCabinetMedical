from django.db import models
from django.core.validators import FileExtensionValidator
from AccountApp.models import Doctor, Patient
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateTimeField()
    reason = models.TextField(max_length=255)
    prescription = models.FileField(
    max_length=255,
    blank=True,
    upload_to='prescriptions/',
    validators=[
        FileExtensionValidator(
            allowed_extensions=['pdf'],
            message="Le fichier doit être au format PDF."
        )
    ]
)
   # status=models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')], default='pending')
   #
    duration = models.PositiveBigIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True )
    updated_at = models.DateTimeField(auto_now=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE,related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE,related_name='appointments')
    Appointment_date = models.DateField(blank=False)
    def clean(self):
        modified_date = self._state.adding or Appointment.objects.filter(pk=self.pk ,Appointment_date=self.Appointment_date).exists()
        if self.Appointment_date < timezone.localdate():
            raise ValidationError("La date de l'appointment ne peut pas être dans le passé.")
    class Meta():
        ordering = ['Appointment_date']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'Appointment_date'],
                name='unique_appointment_per_doctor_per_day',
                violation_error_message="Un docteur ne peut pas avoir deux rendez-vous le même jour.",
            )
        ]
        def __str__(self):
            return f"(self.reason)"

    class status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        CANCELLED = 'cancelled', 'Cancelled'
    status = models.CharField(max_length=20, choices=status.choices, default=status.PENDING)
