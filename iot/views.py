# iot/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import IoTDevice, DeviceData
from .serializers import IoTDeviceSerializer, DeviceDataSerializer


from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

class DeviceConnectView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Add a new IoT device for the authenticated user.",
        request_body=IoTDeviceSerializer,
        responses={201: 'Device created', 200: 'Device already exists', 400: 'Bad request'}
    )
    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response({'error': 'name required'}, status=status.HTTP_400_BAD_REQUEST)
        device, created = IoTDevice.objects.get_or_create(name=name, user=request.user)
        return Response({'status': 'connected', 'device_id': device.id, 'created': created})


class DeviceListView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="List all IoT devices for the authenticated user.",
        responses={200: IoTDeviceSerializer(many=True)}
    )
    def get(self, request):
        devices = IoTDevice.objects.filter(user=request.user)
        serializer = IoTDeviceSerializer(devices, many=True)
        return Response(serializer.data)


class DeviceDetailView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve details for a specific IoT device owned by the authenticated user.",
        responses={200: IoTDeviceSerializer(), 404: 'Device not found'}
    )
    def get(self, request, device_id):
        try:
            device = IoTDevice.objects.get(id=device_id, user=request.user)
        except IoTDevice.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = IoTDeviceSerializer(device)
        return Response(serializer.data)


class DeviceLatestDataView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        operation_description="Retrieve the latest data for a specific IoT device.",
        responses={200: DeviceDataSerializer(), 404: 'Device not found or no data'}
    )
    
    def get(self, request, device_id):
        try:
            device = IoTDevice.objects.get(id=device_id, user=request.user)
        except IoTDevice.DoesNotExist:
            return Response({'error': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)
        all_data = device.data.order_by('-timestamp')
        result = [
            {
                'weight': d.weight,
                'temperature': d.temperature,
                'timestamp': d.timestamp
            } for d in all_data
        ]
        return Response({'data': result})
