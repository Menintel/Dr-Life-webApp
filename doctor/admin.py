from django.contrib import admin
from  doctor import models
# Register your models here.

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'specialization', 'qualification', 'years_experience']

class NotificationAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'appointment', 'type' , 'seen', 'date']

admin.site.register(models.Doctor, DoctorAdmin)
admin.site.register(models.Notification, NotificationAdmin)
