from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from datetime import datetime, timedelta
from datetime import date
from drf_yasg.utils import swagger_auto_schema
from .models import DoseTime, MoodEntry, DoseNote
from .utils import HasSharedAccessOrOwner
import calendar
from rest_framework.views import APIView
from .serializers import (
    DoseTimeSerializer, MoodEntrySerializer, DoseNoteSerializer
)

# ---------- DOSETIME ----------
@swagger_auto_schema(
    methods=['POST'],
    request_body=DoseTimeSerializer,
)
@api_view(['GET', 'POST'])
@permission_classes([HasSharedAccessOrOwner])
def dosetime_list_create(request):
    if request.method == 'GET':
        queryset = DoseTime.objects.filter(user=request.user)  # Filter by user
        serializer = DoseTimeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = DoseTimeSerializer(data=request.data)    
        if serializer.is_valid():
            serializer.save(user=request.user)  # Assign user
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
    

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([HasSharedAccessOrOwner])
def dosetime_detail(request, pk):
    try:
        obj = DoseTime.objects.get(pk=pk, user=request.user)  # Ensure ownership
    except DoseTime.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

    if request.method == 'GET':
        return Response(DoseTimeSerializer(obj).data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = DoseTimeSerializer(obj, data=request.data, partial=(request.method == 'PATCH'))
        if serializer.is_valid():
            serializer.save(user=request.user)  # Re-assign user on update (optional but safe)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=204)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def viewer_dosetime_list(request, user_id):
#     if not has_shared_access(request.user, user_id):
#         return Response({'error': 'Access denied'}, status=403)

#     queryset = DoseTime.objects.filter(user_id=user_id)
#     serializer = DoseTimeSerializer(queryset, many=True)
#     return Response(serializer.data)
# # ---------- PRESCRIPTION ----------
# @swagger_auto_schema(
#     methods=['POST'],
#     request_body = PrescriptionSerializer,
# )
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])  # ensure only logged-in users can access
# def prescription_list_create(request):
#     if request.method == 'GET':
#         queryset = Prescription.objects.filter(user=request.user)  # only show user's prescriptions
#         serializer = gPrescriptionSerializer(queryset, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         data = request.data.copy()
#         data['user'] = request.user.id  # override user field

#         serializer = PrescriptionSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)

# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticated])
# def prescription_detail(request, pk):
#     try:
#         obj = Prescription.objects.get(pk=pk)
#     except Prescription.DoesNotExist:
#         return Response({"error": "Not found"}, status=404)

#     if request.method == 'GET':
#         return Response(gPrescriptionSerializer(obj).data)
#     elif request.method in ['PUT', 'PATCH']:
#         serializer = PrescriptionSerializer(obj, data=request.data, partial=(request.method == 'PATCH'))
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#     elif request.method == 'DELETE':
#         obj.delete()
#         return Response(status=204)

# # ---------- MEDICINE ----------
# @swagger_auto_schema(
#     methods=['POST'],
#     request_body = MedicineSerializer,
# )

# @api_view(['POST', 'GET'])
# @permission_classes([IsAuthenticated])
# def medicine_list_create(request):
#     if request.method == 'GET':
#         medicines = Medicine.objects.all()
#         serializer = MedicineSerializer(medicines, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = MedicineSerializer(data=request.data)
#         if serializer.is_valid():
#             medicine = serializer.save()
#             return Response(MedicineSerializer(medicine).data, status=201)
#         return Response(serializer.errors, status=400)




# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# def medicine_detail(request, pk):
#     try:
#         obj = Medicine.objects.get(pk=pk)
#     except Medicine.DoesNotExist:
#         return Response({"error": "Not found"}, status=404)

#     if request.method == 'GET':
#         return Response(MedicineSerializer(obj).data)
#     elif request.method in ['PUT', 'PATCH']:
#         serializer = MedicineSerializer(obj, data=request.data, partial=(request.method == 'PATCH'))
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)
#     elif request.method == 'DELETE':
#         obj.delete()
#         return Response(status=204)


# # ---------- NOTE ----------
# @swagger_auto_schema(
#     methods=['POST'],
#     request_body = NoteSerializer,
# )

# @api_view(['GET', 'POST'])
# @permission_classes([HasSharedAccessOrOwner])
# def note_list_create(request):
#     if request.method == 'GET':
#         queryset = Note.objects.filter(user=request.user)
#         serializer = NoteSerializer(queryset, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = NoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)  # ✅ Auto-set user
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)



# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# @permission_classes([HasSharedAccessOrOwner])
# def note_detail(request, pk):
#     try:
#         note = Note.objects.get(pk=pk, user=request.user)
#     except Note.DoesNotExist:
#         return Response({"error": "Not found"}, status=404)

#     if request.method == 'GET':
#         return Response(NoteSerializer(note).data)

#     elif request.method in ['PUT', 'PATCH']:
#         serializer = NoteSerializer(note, data=request.data, partial=(request.method == 'PATCH'))
#         if serializer.is_valid():
#             serializer.save(user=request.user)  # ✅ Set user again defensively
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         note.delete()
#         return Response(status=204)
    
#------- Dose Note________
class DoseNoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        dose_time_id = data.get('dose_time_id')
        note = data.get('note', '')
        note_date = data.get('date')  # optional

        if not dose_time_id or not note:
            return Response({"error": "dose_time_id and note are required."}, status=400)

        try:
            dose_time = DoseTime.objects.get(id=dose_time_id, user=request.user)
        except DoseTime.DoesNotExist:
            return Response({"error": "DoseTime not found or not accessible."}, status=404)

        try:
            save_date = date.fromisoformat(note_date) if note_date else date.today()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        dose_note = DoseNote.objects.create(
            user=request.user,
            dose_time=dose_time,
            note=note,
            date=save_date
        )

        return Response(DoseNoteSerializer(dose_note).data, status=status.HTTP_201_CREATED)

    def get(self, request):
        note_date = request.query_params.get('date')
        dose_time_id = request.query_params.get('dose_time_id')

        filters = {'user': request.user}

        if note_date:
            try:
                filters['date'] = date.fromisoformat(note_date)
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        if dose_time_id:
            filters['dose_time__id'] = dose_time_id

        notes = DoseNote.objects.filter(**filters).order_by('-date')
        serializer = DoseNoteSerializer(notes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
# ---------- DAY SUMMARY ----------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_day_summary(request, date_str):
    user = request.user
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

    weekday_key = calendar.day_abbr[date.weekday()].lower()[:3]

    # Get mood
    try:
        mood = MoodEntry.objects.get(user=user, date=date)
        mood_data = MoodEntrySerializer(mood).data
    except MoodEntry.DoesNotExist:
        mood_data = None

    # Get DoseTimes and related DoseNotes for that date
    dosetimes = DoseTime.objects.filter(user=user)
    dosetime_notes = []

    for dt in dosetimes:
        note = DoseNote.objects.filter(user=user, dose_time=dt, date=date).first()
        note_data = DoseNoteSerializer(note).data if note else None

        dosetime_notes.append({
            "id": dt.id,
            "name": dt.name,
            "start_time": dt.start_time,
            "end_time": dt.end_time,
            "note": note_data
        })

    return Response({
        "date": date_str,
        "dosetimes": dosetime_notes,
        "mood": mood_data
    })
# ---------- BULK MEDICINE ----------
# @swagger_auto_schema(
#     methods=['POST'],
#     request_body = BulkMedicineSerializer,
# )

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def bulk_create_medicines(request):
#     serializer = BulkMedicineSerializer(data=request.data)
#     if serializer.is_valid():
#         medicines = serializer.save()
#         # Serialize the created medicines for response
#         response_serializer = MedicineSerializer(medicines, many=True)
#         return Response(response_serializer.data, status=201)
#     return Response(serializer.errors, status=400)

@swagger_auto_schema(
    methods=['POST'],
    request_body=MoodEntrySerializer,
)
@api_view(['GET', 'POST', 'PATCH', 'DELETE'])
@permission_classes([HasSharedAccessOrOwner])
def today_mood(request):
    today = date.today()
    user = request.user

    if request.method == 'GET':
        try:
            mood = MoodEntry.objects.get(user=user, date=today)
            serializer = MoodEntrySerializer(mood)
            return Response(serializer.data)
        except MoodEntry.DoesNotExist:
            return Response({"message": "No mood saved for today."}, status=404)

    elif request.method == 'POST':
        emoji = request.data.get('emoji')
        if not emoji:
            return Response({"error": "Emoji is required"}, status=400)

        mood, created = MoodEntry.objects.update_or_create(
            user=user,
            date=today,
            defaults={'emoji': emoji}
        )
        return Response({
            "message": "Mood created" if created else "Mood updated",
            "emoji": emoji,
            "date": today.isoformat()
        }, status=201 if created else 200)

    elif request.method == 'PATCH':
        emoji = request.data.get('emoji')
        if not emoji:
            return Response({"error": "Emoji is required"}, status=400)

        try:
            mood = MoodEntry.objects.get(user=user, date=today)
            mood.emoji = emoji
            mood.save()
            return Response({
                "message": "Mood updated",
                "emoji": mood.emoji,
                "date": mood.date.isoformat()
            })
        except MoodEntry.DoesNotExist:
            return Response({"error": "No mood entry found for today"}, status=404)

    elif request.method == 'DELETE':
        deleted, _ = MoodEntry.objects.filter(user=user, date=today).delete()
        if deleted:
            return Response({"message": "Mood entry deleted"})
        else:
            return Response({"message": "No mood to delete"}, status=404)
        
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def viewer_note_list_create(request, user_id):
#     if not has_shared_access(request.user, user_id):
#         return Response({'error': 'Access denied'}, status=403)
    
#     notes = Note.objects.filter(user_id=user_id)
#     serializer = NoteSerializer(notes, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def viewer_today_mood(request, user_id):
#     if not has_shared_access(request.user, user_id):
#         return Response({'error': 'Access denied'}, status=403)
    
#     # Fetch mood entry for today
#     today = date.today()
#     mood_entry = MoodEntry.objects.filter(user_id=user_id, date=today).first()
#     if not mood_entry:
#         return Response({'message': 'No mood entry found'}, status=404)

#     serializer = MoodEntrySerializer(mood_entry)
#     return Response(serializer.data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def viewer_dosetime_list(request, user_id):
#     if not has_shared_access(request.user, user_id):
#         return Response({'error': 'Access denied'}, status=403)

#     dosetimes = DoseTime.objects.filter(user_id=user_id)
#     serializer = DoseTimeSerializer(dosetimes, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def viewer_day_summary(request, date_str, user_id):
#     if not has_shared_access(request.user, user_id):
#         return Response({"error": "Access denied"}, status=403)

#     try:
#         date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
#     except ValueError:
#         return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

#     weekday_key = calendar.day_abbr[date_obj.weekday()].lower()[:3]

#     # Notes
#     all_notes = Note.objects.filter(user_id=user_id, start_datetime__date__lte=date_obj)
#     visible_notes = []

#     for note in all_notes:
#         start_date = note.start_datetime.date()

#         if note.end_date:
#             end_date = note.end_date
#         elif note.duration_in_days:
#             end_date = start_date + timedelta(days=note.duration_in_days - 1)
#         else:
#             end_date = None  # Repeats indefinitely

#         if start_date <= date_obj and (end_date is None or date_obj <= end_date):
#             if not note.repeat_days or weekday_key in note.repeat_days:
#                 visible_notes.append(note)

#     # MoodEntry
#     try:
#         mood = MoodEntry.objects.get(user_id=user_id, date=date_obj)
#         mood_data = MoodEntrySerializer(mood).data
#     except MoodEntry.DoesNotExist:
#         mood_data = None

#     # DoseTime
#     dosetime = DoseTime.objects.filter(user_id=user_id)
#     dosetime_data = DoseTimeSerializer(dosetime, many=True).data

#     return Response({
#         "date": date_str,
#         "dosetime": dosetime_data,
#         "notes": NoteSerializer(visible_notes, many=True).data,
#         "mood": mood_data
#     })
