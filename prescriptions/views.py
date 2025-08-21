import os
import tempfile
from datetime import datetime, date

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import serializers

from .models import Prescription, MedicineInfo
from .serializers import PrescriptionSerializer
from .ocr_engine import extract_prescription_info


# Serializers for Swagger documentation
class MedicineRequestSerializer(serializers.Serializer):
    medicine_name = serializers.CharField(
        max_length=255, 
        help_text="Name of the medicine",
        default="Lisinopril"
    )
    generic_name = serializers.CharField(
        max_length=255, 
        help_text="Generic name of the medicine",
        default="Lisinopril"
    )
    instructions = serializers.CharField(
        help_text="Instructions for taking the medicine",
        default="Take 1 tablet by mouth daily"
    )
    qty = serializers.CharField(
        max_length=20, 
        help_text="Quantity prescribed",
        default="30"
    )
    refills_info = serializers.CharField(
        max_length=255, 
        help_text="Refill information",
        default="5 refills remaining"
    )
    side_effects = serializers.CharField(
        help_text="Known side effects",
        default="Dizziness, dry cough"
    )


class PrescriptionRequestSerializer(serializers.Serializer):
    rx_number = serializers.CharField(
        max_length=50, 
        required=False, 
        help_text="Prescription number",
        default="RX123456789"
    )
    store_number = serializers.CharField(
        max_length=50, 
        required=False, 
        help_text="Store/Department number",
        default="1234"
    )
    pharmacy_or_doctor_name = serializers.CharField(
        max_length=255, 
        required=False, 
        help_text="Pharmacy or doctor name",
        default="CVS Pharmacy"
    )
    contact_details = serializers.CharField(
        max_length=255, 
        required=False, 
        help_text="Contact details",
        default="(555) 123-4567"
    )
    date_filled = serializers.CharField(
        max_length=50, 
        required=False, 
        help_text="Date filled (MM/DD/YYYY or YYYY-MM-DD)",
        default="07/20/2025"
    )
    date_expired = serializers.CharField(
        max_length=50, 
        required=False, 
        help_text="Expiration date",
        default="07/20/2026"
    )
    address = serializers.CharField(
        required=False, 
        help_text="Address",
        default="123 Main St, City, State 12345"
    )
    medicines_names = MedicineRequestSerializer(
        many=True, 
        required=False, 
        help_text="List of medicines in the prescription"
    )


class OCRResponseSerializer(serializers.Serializer):
    rx_number = serializers.CharField(required=False)
    store_number = serializers.CharField(required=False)
    pharmacy_or_doctor_name = serializers.CharField(required=False)
    contact_details = serializers.CharField(required=False)
    date_filled = serializers.CharField(required=False)
    date_expired = serializers.CharField(required=False)
    address = serializers.CharField(required=False)
    medicines_names = MedicineRequestSerializer(many=True, required=False)


class ErrorResponseSerializer(serializers.Serializer):
    error = serializers.CharField(help_text="Error message")


#@permission_classes([IsAuthenticated])
class ExtractPrescriptionOCRView(APIView):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        operation_description="Extract prescription information from uploaded images using OCR",
        operation_summary="OCR Prescription Extraction",
        manual_parameters=[
            openapi.Parameter(
                'image',
                openapi.IN_FORM,
                description="One or more prescription images to process",
                type=openapi.TYPE_FILE,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Successfully extracted prescription information",
                schema=OCRResponseSerializer()
            ),
            400: openapi.Response(
                description="Bad request - no image files provided",
                schema=ErrorResponseSerializer()
            ),
            500: openapi.Response(
                description="Internal server error during OCR processing",
                schema=ErrorResponseSerializer()
            )
        },
        tags=['Prescriptions'],
        security=[{'Bearer': []}]
    )
    def post(self, request):
        images = request.FILES.getlist("image")
        if not images:
            return Response({"error": "Image file(s) required."}, status=400)

        temp_paths = []
        try:
            # Save uploaded images temporarily
            for image in images:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                    for chunk in image.chunks():
                        tmp.write(chunk)
                    temp_paths.append(tmp.name)

            # OCR extraction
            extracted = extract_prescription_info(image_paths=temp_paths)
            if "error" in extracted:
                return Response(extracted, status=500)

            return Response(extracted, status=200)

        finally:
            for path in temp_paths:
                if os.path.exists(path):
                    os.remove(path)


#@permission_classes([IsAuthenticated])
class SubmitPrescriptionView(APIView):
    parser_classes = [JSONParser]

    @swagger_auto_schema(
        operation_description="Submit a new prescription with medicine details",
        operation_summary="Create New Prescription",
        request_body=PrescriptionRequestSerializer,
        responses={
            201: openapi.Response(
                description="Prescription created successfully",
                schema=PrescriptionSerializer()
            ),
            400: openapi.Response(
                description="Bad request - invalid data provided",
                schema=ErrorResponseSerializer()
            )
        },
        tags=['Prescriptions'],
        security=[{'Bearer': []}]
    )
    def post(self, request):
        data = request.data
        raw_dob = data.get("date_filled", "2000-01-01")

        try:
            dob = datetime.strptime(raw_dob, "%m/%d/%Y").date()
        except ValueError:
            try:
                dob = datetime.strptime(raw_dob, "%Y-%m-%d").date()
            except ValueError:
                dob = date(2000, 1, 1)

        prescription = Prescription.objects.create(
            user=request.user,
            rx_number=data.get("rx_number"),
            department_number=data.get("store_number"),
            dob=dob,
            pharmacy_or_doctor_name=data.get("pharmacy_or_doctor_name", ""),
            contact_details=data.get("contact_details", ""),
            date_filled=data.get("date_filled", ""),
            date_expired=data.get("date_expired", ""),
            address=data.get("address", ""),
            store_number=data.get("store_number", ""),
            rx_image=None  # Optional: save image later or base64 if sent
        )

        for med in data.get("medicines_names", []):
            MedicineInfo.objects.create(
                prescription=prescription,
                medicine_name=med.get("medicine_name", ""),
                generic_name=med.get("generic_name", ""),
                instructions=med.get("instructions", ""),
                qty=med.get("qty", ""),
                refills_info=med.get("refills_info", ""),
                side_effects=med.get("side_effects", "")
            )

        return Response(PrescriptionSerializer(prescription).data, status=status.HTTP_201_CREATED)

#@permission_classes([IsAuthenticated])
class UserPrescriptionsView(APIView):
    @swagger_auto_schema(
        operation_description="Get all prescriptions for the authenticated user",
        operation_summary="List User Prescriptions",
        responses={
            200: openapi.Response(
                description="List of user prescriptions",
                schema=PrescriptionSerializer(many=True)
            )
        },
        tags=['Prescriptions'],
        security=[{'Bearer': []}]
    )
    def get(self, request):
        prescriptions = Prescription.objects.filter(user=request.user).order_by('-created_at')
        serializer = PrescriptionSerializer(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def viewer_get_prescription(request, user_id):
#     if not has_shared_access(request.user, user_id):
#         return Response({"error": "Access denied"}, status=403)

#     dob = request.query_params.get("dob")
#     rx_number = request.query_params.get("rx_number")
#     department_number = request.query_params.get("department_number")

#     if not dob or not rx_number or not department_number:
#         return Response(
#             {"error": "DOB, RX number, and department number are all required."},
#             status=400
#         )

#     try:
#         dob = datetime.strptime(dob, "%Y-%m-%d").date()
#     except ValueError:
#         return Response({"error": "DOB format must be YYYY-MM-DD"}, status=400)

#     filters = {
#         "user_id": user_id,
#         "dob": dob,
#         "rx_number": rx_number,
#         "department_number": department_number,
#     }

#     try:
#         prescription = Prescription.objects.get(**filters)
#         return Response(PrescriptionSerializer(prescription).data)
#     except Prescription.DoesNotExist:
#         return Response({"error": "Prescription not found."}, status=404)
