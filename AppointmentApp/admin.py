from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('reason', 'status', 'Appointment_date')
    list_filter = ('status', 'reason')
    
    
