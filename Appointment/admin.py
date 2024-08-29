from django.contrib import admin
from .models import Appointment
# Register your models here.

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id','business_id','email','user','date','time')

admin.site.register(Appointment,AppointmentAdmin)