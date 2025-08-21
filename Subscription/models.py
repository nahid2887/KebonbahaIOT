from django.db import models
import shortuuid
from django.contrib.auth.models import User


# Create your models here.
def generate_random_id():
    return shortuuid.uuid()[:4]



class SubscriptionModel(models.Model):
    class PackageType(models.TextChoices):
        FREE = 'Free', 'Free'
        MONTHLY = 'Monthly', 'Monthly'
        YEARLY = 'Yearly', 'Yearly'

    class PackageStatus(models.TextChoices):
        ACTIVE = 'Active', 'Active'
        POSTPONE = 'Postpone', 'Postpone'

    id = models.CharField(
        primary_key=True,
        max_length=10,
        default=generate_random_id,
        # editable=False
    )
    package_type = models.CharField(
        max_length=10,
        choices=PackageType.choices,
        default=PackageType.FREE
    )
    package_status = models.CharField(
        max_length=10,
        choices=PackageStatus.choices,
        default=PackageStatus.POSTPONE
    )
    package_amount = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Type: {self.package_type} - Status: {self.package_status}"
    

class UserSubscriptionModel(models.Model):
    class PackageType(models.TextChoices):
        FREE = 'Free', 'Free'
        MONTHLY = 'Monthly', 'Monthly'
        YEARLY = 'Yearly', 'Yearly'

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='package')  # Fixed typo
    package_type = models.CharField(
        max_length=10,
        choices=PackageType.choices,
        default=PackageType.FREE
    )
    is_active = models.BooleanField(default=False)
    package_start_date = models.DateField(null=True, blank=True)
    package_end_date = models.DateField(null=True, blank=True)
    package_amount = models.PositiveIntegerField(default=0)
    

    def __str__(self):
        return f"{self.user} - package type: {self.package_type}"
    

class Total_revenue(models.Model):
        total_revenue = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
        
        def __str__(self):
            return f"{self.total_revenue}"
        

