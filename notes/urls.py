from django.urls import path
from .views import (
    dosetime_list_create, dosetime_detail,
    
    # note_list_create, note_detail,
    get_day_summary, 
    today_mood,
    DoseNoteView
    # viewer_note_list_create,
    # viewer_today_mood,
    # viewer_dosetime_list,
    # viewer_day_summary
)

urlpatterns = [
    # DoseTime
    path('dosetime/', dosetime_list_create, name='dosetime-list-create'),
    path('dosetime/<int:pk>/', dosetime_detail, name='dosetime-detail'),
    

    # # Prescription
    # path('prescription/', prescription_list_create, name='prescription-list-create'),
    # path('prescription/<int:pk>/', prescription_detail, name='prescription-detail'),

    # # Medicine
    # path('medicine/', medicine_list_create, name='medicine-list-create'),
    # path('medicine/<int:pk>/', medicine_detail, name='medicine-detail'),
    # path('medicine/bulk/', bulk_create_medicines, name='bulk-create-medicines'),

    # # Note
    # path('note/', note_list_create, name='note-list-create'),
    # path('note/<int:pk>/', note_detail, name='note-detail'),

    # Summary
    path('summary/<str:date_str>/', get_day_summary, name='get-day-summary'),
    path('mood/', today_mood, name='today_mood'),
     path('dose-notes/', DoseNoteView.as_view(), name='dose-notes'),


    # #viwes
    # path('viewer/note/<int:user_id>/', viewer_note_list_create, name='viewer-note-list-create'),
    # path('viewer/mood/<int:user_id>/', viewer_today_mood, name='viewer-today-mood'),
    # path('viewer/dosetime/<int:user_id>/', viewer_dosetime_list, name='viewer-dosetime-list'),
    # path('viewer/summary/<str:date_str>/<int:user_id>/', viewer_day_summary, name='viewer-day-summary'),


]
