from django.db import models
from django.contrib.auth.models import User

class Prescription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rx_number = models.CharField(max_length=50, blank=True, null=True)
    department_number = models.CharField(max_length=4, blank=True, null=True)
    dob = models.DateField()
    pharmacy_or_doctor_name = models.CharField(max_length=255)
    contact_details = models.CharField(max_length=255)
    date_filled = models.CharField(max_length=50)
    date_expired = models.CharField(max_length=50)
    address = models.TextField()
    store_number = models.CharField(max_length=50)

    rx_image = models.ImageField(upload_to='prescriptions/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prescription (RX: {self.rx_number or 'N/A'}, Dept: {self.department_number or 'N/A'})"

class MedicineInfo(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')

    medicine_name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255)
    instructions = models.TextField()
    qty = models.CharField(max_length=20)
    refills_info = models.CharField(max_length=255)
    side_effects = models.TextField()

    def __str__(self):
        return f"Medicine: {self.medicine_name}"
