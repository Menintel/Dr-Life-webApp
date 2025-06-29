from django.db import models
from shortuuid.django_fields import ShortUUIDField

from doctor import models as doctor_models
from patient import models as patient_models

# Create your models here.
class Service(models.Model):
    image = models.ImageField(upload_to="images", null=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    available_doctors = models.ManyToManyField(doctor_models.Doctor, blank=True)

    def __str__(self):
        return f"{self.name} - {self.cost}"
    
class Appointment(models.Model):
    STATUS = [
        ('Scheduled','Scheduled'),
        ('Completed','Completed'),
        ('Pending','Pending'),
        ('Cancelled','Cancelled'),
    ]

    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_app')
    doctor = models.ForeignKey(doctor_models.Doctor, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_app')
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name='service_app')
    appointment_date = models.DateTimeField(null=True, blank=True)
    issues = models.TextField(blank=True, null=True)
    symptoms = models.TextField(blank=True, null=True)
    appointment_id = ShortUUIDField(length=6, max_length=10, alphabet="1234567890")
    status = models.CharField(max_length=120, choices=STATUS)

    def __str__(self):
        return f"{self.patient.user.first_name} {self.patient.user.last_name} with {self.doctor.user.first_name} {self.doctor.user.last_name}"
    

class MedicalRecord(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    treatment = models.TextField()

    def __str__(self):
        return f"Medical Record for {self.appointment.patient.user.first_name} {self.appointment.patient.user.last_name}"
    
class LabTest(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.test_name}"
    
class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    medications = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Prescription for {self.appointment.patient.user.first_name} {self.appointment.patient.user.last_name}"
    
class Billing(models.Model):
    patient = models.ForeignKey(patient_models.Patient, on_delete=models.SET_NULL, null=True, blank=True, related_name="billing")
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='billing', blank=True, null=True)
    sub_total = models.DecimalField(max_digits=10, decimal_places=2)
    tax = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=[('Paid','Paid'),('Unpaid','Unpaid')])
    billing_id = ShortUUIDField(length=6, max_length=10, alphabet ='1234567890')

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        patient_name = self.patient.user.last_name if self.patient else "Deleted Patient"
        return f"Billing for {patient_name} - Total: {self.total}"