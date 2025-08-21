from django.urls import path
from .views import (
    SendOTP, VerifyOTP,
    ShareAccess, WhoICanView, WhoCanViewMe,
    RespondToAccessRequest, MyPendingAccessRequests
)

urlpatterns = [
    path('send-otp/', SendOTP.as_view()),
    path('verify-otp/', VerifyOTP.as_view()),
    path('share-access/', ShareAccess.as_view()),
    path('who-i-can-view/', WhoICanView.as_view()),
    path('who-can-view-me/', WhoCanViewMe.as_view()),
    path('respond-to-access/', RespondToAccessRequest.as_view()),  # ✅ new
    path('my-pending-requests/', MyPendingAccessRequests.as_view()),  # ✅ new
]