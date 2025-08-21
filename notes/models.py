from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import time, timedelta
from django.utils import timezone
from datetime import date


class DoseTime(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    end_time = models.TimeField()
   #user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# class Prescription(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     doctor_name = models.CharField(max_length=100)
#     prescription_number = models.CharField(max_length=50)
#     store_name = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.prescription_number} - {self.doctor_name}"

# class Medicine(models.Model):
#     prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')
#     name = models.CharField(max_length=100)
#     info = models.TextField()
#     side_effects = models.TextField(blank=True)
#     dose_times = models.ManyToManyField(DoseTime)
#     days = models.PositiveIntegerField()
#     total_quantity = models.PositiveIntegerField(blank=True, null=True)

#     def __str__(self):
#         return self.name
    

# class Note(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     start_datetime = models.DateTimeField(default=timezone.now)  # The date of the event
#     event_time = models.TimeField(default=time(9, 0))           # The time of the event, e.g. 09:00 AM

#     # Optional end date or duration (for recurring or time ranges)
#     end_date = models.DateField(blank=True, null=True)
#     duration_in_days = models.PositiveIntegerField(blank=True, null=True)

#     # Repeat days etc.
#     REPEAT_DAYS = [
#         ('sun', 'Sunday'),
#         ('mon', 'Monday'),
#         ('tue', 'Tuesday'),
#         ('wed', 'Wednesday'),
#         ('thu', 'Thursday'),
#         ('fri', 'Friday'),
#         ('sat', 'Saturday'),
#     ]
#     repeat_days = models.JSONField(blank=True, null=True)

#     content = models.TextField()

#     def __str__(self):
#         return f"{self.user.username} - {self.start_datetime} {self.event_time.strftime('%I:%M %p').lstrip('0')}"

#     def is_repeating_every_day(self):
#         """
#         Returns True if the note has no end date, no duration, and no repeat days.
#         This means it should repeat daily until deleted.
#         """
#         return self.end_datetime is None and self.duration_in_days is None and not self.repeat_days

#     def get_end_datetime(self):
#         """
#         Calculates and returns the effective end datetime of the note.
#         """
#         if self.end_datetime:
#             return self.end_datetime
#         elif self.duration_in_days:
#             return self.start_datetime + timedelta(days=self.duration_in_days)
#         else:
#             return None  # Means repeat indefinitely

#     def clean(self):
#         """
#         Ensures that repeat_days only contains valid day keys.
#         """
#         super().clean()
#         if self.repeat_days:
#             invalid = [day for day in self.repeat_days if day not in self.VALID_REPEAT_KEYS]
#             if invalid:
#                 raise ValidationError({'repeat_days': f"Invalid day(s): {', '.join(invalid)}"})



class MoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    emoji = models.CharField(max_length=10)

    class Meta:
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.emoji}"
    



class DoseNote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dose_time = models.ForeignKey(DoseTime, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.dose_time.name} on {self.date}"