from django.contrib import admin
from .models import Warehouse, PostalOffice, FullIndex


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('warehouse_name', 'city_name', 'region_name', 'index')
    search_fields = ('warehouse_name', 'city_name', 'region_name')


@admin.register(FullIndex)
class FullIndexAdmin(admin.ModelAdmin):
    list_display = ('index', 'region', 'comments')
    search_fields = ("index", 'comments')


@admin.register(PostalOffice)
class PostalOfficeAdmin(admin.ModelAdmin):
    list_display = ('index', 'name_uz', 'region', 'city', 'working_days')
    search_fields = ('name_uz', 'region', 'city')
