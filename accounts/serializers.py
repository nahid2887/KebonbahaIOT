from rest_framework import serializers
from .models import PhoneOTP, SharedAccess

class PhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)

class OTPVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)



class SharedAccessSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedAccess
        fields = ['id', 'owner', 'viewer', 'status']
