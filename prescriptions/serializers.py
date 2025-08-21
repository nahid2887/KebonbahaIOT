from rest_framework import serializers
from .models import Prescription, MedicineInfo

class MedicineInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineInfo
        fields = '__all__'
        extra_kwargs = {
            'prescription': {'read_only': True}  # Prevent client from injecting invalid prescriptions
        }

class PrescriptionSerializer(serializers.ModelSerializer):
    medicines = MedicineInfoSerializer(many=True, read_only=True)
    medicines_data = MedicineInfoSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Prescription
        fields = [
            'id',
            'rx_number',
            'department_number',
            'dob',
            'pharmacy_or_doctor_name',
            'contact_details',
            'date_filled',
            'date_expired',
            'address',
            'store_number',
            'rx_image',
            'created_at',
            'medicines',
            'medicines_data'
        ]
        extra_kwargs = {
            'created_at': {'read_only': True}
        }

    def create(self, validated_data):
        medicines_data = validated_data.pop('medicines_data', [])
        user = self.context['request'].user  # Injected from view
        prescription = Prescription.objects.create(user=user, **validated_data)

        for med_data in medicines_data:
            MedicineInfo.objects.create(prescription=prescription, **med_data)

        return prescription
