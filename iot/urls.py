from django.urls import path
from .views import DeviceConnectView, DeviceLatestDataView, DeviceListView, DeviceDetailView

urlpatterns = [
    path('connect/', DeviceConnectView.as_view(), name='device-connect'),
    path('devices/', DeviceListView.as_view(), name='device-list'),
    path('devices/<int:device_id>/', DeviceDetailView.as_view(), name='device-detail'),
    path('data/<int:device_id>/', DeviceLatestDataView.as_view(), name='device-latest-data'),
]
