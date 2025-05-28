from django.contrib import admin
from patient import models
# Register your models here.

class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'mobile', 'gender', 'dob']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'appointment', 'type' , 'seen', 'date']

admin.site.register(models.Patient, PatientAdmin)
admin.site.register(models.Notification, NotificationAdmin)