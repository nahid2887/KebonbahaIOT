from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone

class PhoneOTP(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return (timezone.now() - self.created_at).total_seconds() < 120

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    e_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

class SharedAccess(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_with')
    viewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='can_view')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('owner', 'viewer')