from rest_framework import serializers
from .models import DoseTime,   MoodEntry , DoseNote
class DoseTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoseTime
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True}  # 👈 prevents DRF from requiring 'user' in the input
        }

# class MedicineSerializer(serializers.ModelSerializer):
#     prescription = serializers.PrimaryKeyRelatedField(queryset=Prescription.objects.all())
#     dose_times = DoseTimeSerializer(many=True, read_only=True)  # for response
#     dose_time_ids = serializers.PrimaryKeyRelatedField(
#         queryset=DoseTime.objects.all(),
#         many=True,
#         write_only=True,
#         required=True
#     )

#     class Meta:
#         model = Medicine
#         fields = [
#             'id', 'prescription', 'name', 'info', 'side_effects',
#             'days', 'total_quantity', 'dose_times', 'dose_time_ids'
#         ]

#     def create(self, validated_data):
#         dose_time_ids = validated_data.pop('dose_time_ids')
#         medicine = Medicine.objects.create(**validated_data)
#         medicine.dose_times.set(dose_time_ids)
#         medicine.total_quantity = medicine.days * len(dose_time_ids)
#         medicine.save()
#         return medicine

# class NoteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Note
#         fields = '__all__'
#         extra_kwargs = {
#             'user': {'read_only': True}  # user is set automatically; not from input
#         }

# class BulkMedicineSerializer(serializers.Serializer):
#     medicines = MedicineSerializer(many=True)

#     def create(self, validated_data):
#         medicines_data = validated_data['medicines']
#         created_medicines = []
#         for medicine_data in medicines_data:
#             dose_time_ids = medicine_data.pop('dose_time_ids')
#             medicine = Medicine.objects.create(**medicine_data)
#             medicine.dose_times.set(dose_time_ids)
#             medicine.total_quantity = medicine.days * len(dose_time_ids)
#             medicine.save()
#             created_medicines.append(medicine)
#         return created_medicines
    
# class gPrescriptionSerializer(serializers.ModelSerializer):
#     medicines = MedicineSerializer(many=True, read_only=True)  # related_name from model

#     class Meta:
#         model = Prescription
#         fields = ['id', 'doctor_name', 'prescription_number', 'store_name', 'created_at', 'medicines']
# # class PrescriptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Prescription
#         fields = '__all__'
#         extra_kwargs = {
#             'user': {'required': False}
#         }


class MoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodEntry
        fields = ['date', 'emoji', 'user']
        extra_kwargs = {
            'user': {'read_only': True}
        }



class DoseNoteSerializer(serializers.ModelSerializer):
    dose_time_name = serializers.CharField(source='dose_time.name', read_only=True)

    class Meta:
        model = DoseNote
        fields = ['id', 'dose_time', 'dose_time_name', 'note', 'date']