from django.contrib import admin
from .models import Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('warehouse_name', 'city_name', 'region_name', 'index')
    search_fields = ('warehouse_name', 'city_name', 'region_name')
