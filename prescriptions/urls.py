from django.urls import path
from .views import (
    ExtractPrescriptionOCRView,
    SubmitPrescriptionView,
    UserPrescriptionsView,
)

urlpatterns = [
    path('extract-prescription/', ExtractPrescriptionOCRView.as_view()),
    path('submit-prescription/', SubmitPrescriptionView.as_view()),
    path('my-prescriptions/', UserPrescriptionsView.as_view()),
]
