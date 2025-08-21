# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Medicine, Note
# from datetime import datetime

# @receiver(post_save, sender=Medicine)
# def create_note_for_medicine(sender, instance, created, **kwargs):
#     if created:
#         user = instance.prescription.user
#         content = f"Start taking medicine: {instance.name}"
#         Note.objects.create(
#             user=user,
#             start_datetime=datetime.now(),
#             content=content
#         )
