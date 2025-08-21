from rest_framework import serializers

from .models import SubscriptionModel,UserSubscriptionModel,Total_revenue


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionModel
        fields = "__all__"
        

        
class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscriptionModel
        fields = ["package_type","is_active","package_start_date","package_end_date","package_amount"]


class TotalRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Total_revenue
        fields = ['id','total_revenue']