from django.contrib import admin
from .models import IoTDevice, DeviceData

@admin.register(IoTDevice)
class IoTDeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'last_seen')
    search_fields = ('name',)

@admin.register(DeviceData)
class DeviceDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'weight', 'temperature', 'timestamp')
    search_fields = ('device__name',)
    list_filter = ('timestamp',)