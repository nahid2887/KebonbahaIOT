import random
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import PhoneOTP, SharedAccess
from .serializers import PhoneSerializer, OTPVerifySerializer
from .utils import send_otp_via_sms
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SendOTP(APIView):
    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Signup using full name, email, mobile, and password.",
        request_body=PhoneSerializer,
        responses={
            201: openapi.Response("User created successfully"),
            400: openapi.Response("Bad request (validation errors)")
        })
    def post(self, request):
        serializer = PhoneSerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            otp = str(random.randint(100000, 999999))
            PhoneOTP.objects.update_or_create(phone=phone, defaults={'otp': otp})
            if send_otp_via_sms(phone, otp):
                return Response({'message': 'OTP sent', 'otp': otp})
        return Response({'error': 'Invalid phone or failed'}, status=400)

class VerifyOTP(APIView):
    @swagger_auto_schema(
        operation_summary="Register a new user",
        operation_description="Signup using full name, email, mobile, and password.",
        request_body=OTPVerifySerializer,
        responses={
            201: openapi.Response("User created successfully"),
            400: openapi.Response("Bad request (validation errors)")
        })
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            phone = serializer.validated_data['phone']
            otp = serializer.validated_data['otp']
            try:
                record = PhoneOTP.objects.get(phone=phone, otp=otp)
                if not record.is_valid():
                    record.delete()
                    return Response({'error': 'OTP expired'}, status=400)
                user, created = User.objects.get_or_create(username=phone)
                refresh = RefreshToken.for_user(user)
                record.delete()
                return Response({
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'id':user.id,
                    'new_user': created
                })
            except PhoneOTP.DoesNotExist:
                return Response({'error': 'Invalid OTP'}, status=400)
        return Response(serializer.errors, status=400)

class ShareAccess(APIView):
    
    permission_classes = [IsAuthenticated]
    def post(self, request):
        viewer_id = request.data.get("viewer_id")
        try:
            viewer = User.objects.get(id=viewer_id)
            access, created = SharedAccess.objects.get_or_create(owner=request.user, viewer=viewer)
            if not created and access.status == 'accepted':
                return Response({"message": "Access already accepted"})
            access.status = 'pending'
            access.save()
            return Response({"message": "Access request sent"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class RespondToAccessRequest(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        owner_id = request.data.get("owner_id")
        action = request.data.get("action")  # 'accept' or 'reject'

        try:
            access = SharedAccess.objects.get(owner_id=owner_id, viewer=request.user)
            if action == 'accept':
                access.status = 'accepted'
                message = "Access accepted"
            elif action == 'reject':
                access.status = 'rejected'
                message = "Access rejected"
            else:
                return Response({"error": "Invalid action"}, status=400)

            access.save()
            return Response({"message": message})
        except SharedAccess.DoesNotExist:
            return Response({"error": "Access request not found"}, status=404)

class WhoICanView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        owners = User.objects.filter(shared_with__viewer=request.user, shared_with__status='accepted')
        return Response([{'username': u.username, 'id': u.id} for u in owners])

class WhoCanViewMe(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        viewers = User.objects.filter(can_view__owner=request.user, can_view__status='accepted')
        return Response([{'username': u.username, 'id': u.id} for u in viewers])

class MyPendingAccessRequests(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pending_requests = SharedAccess.objects.filter(viewer=request.user, status='pending')
        return Response([
            {'owner_id': req.owner.id, 'owner_username': req.owner.username}
            for req in pending_requests
        ])