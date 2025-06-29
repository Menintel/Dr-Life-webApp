from django.db import models
from django.utils import timezone

from userauths import models as userauths_models

NOTIFICATION_TYPE = (
    ("New Appointment","New Appointment"),
    ("Appointment Cancelled","Appointment Cancelled"),
)

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(userauths_models.User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    qualification = models.CharField(max_length=100, null=True, blank=True)
    years_experience = models.CharField(max_length=100, null=True, blank=True)
    next_available_appointment_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"


class Notification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey("base.Appointment", on_delete=models.CASCADE, null=True, blank=True , related_name="appointment_notification")
    type = models.CharField(max_length=100, choices=None)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)  

    class Meta:
        verbose_name_plural = "Notification"

    def __str__(self):
        return f"Dr {self.doctor.user.first_name} {self.doctor.user.last_name} Notification"