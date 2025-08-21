from django.contrib import admin

# Register your models here.
from .models import SubscriptionModel,UserSubscriptionModel,Total_revenue
# Register your models here.

admin.site.register(SubscriptionModel)
admin.site.register(UserSubscriptionModel)
admin.site.register(Total_revenue)