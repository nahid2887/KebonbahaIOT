from django.db import models
from django.contrib.auth.models import User

class IoTDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=100, unique=True)
    last_seen = models.DateTimeField(auto_now=True)

class DeviceData(models.Model):
    device = models.ForeignKey(IoTDevice, on_delete=models.CASCADE, related_name='data')
    weight = models.FloatField()
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
