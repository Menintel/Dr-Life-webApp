from django.db import models
from django.conf import settings
from django.utils import timezone
from userauths import models as userauths_models

NOTIFICATION_TYPE = (
    ("Appointment Scheduled","Appointment Scheduled"),
    ("Appointment Cancelled","Appointment Cancelled"),
)

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

# Create your models here.
class Patient(models.Model):
    user = models.OneToOneField(userauths_models.User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images", null=True, blank=True)
    mobile = models.CharField(max_length=15, null=True, blank=True,)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def age(self):
        today = timezone.now().date()
        return today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))


class Notification(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.SET_NULL, null=True, blank=True)
    appointment = models.ForeignKey("base.Appointment", on_delete=models.CASCADE, null=True, blank=True , related_name="patient_appointment_notification")
    type = models.CharField(max_length=100, choices=None)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Notification"

    def __str__(self):
        return f"{self.patient.user.first_name} {self.patient.user.last_name} Notification"