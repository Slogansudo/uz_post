from django.db import models


class Warehouse(models.Model):
    warehouse_name = models.CharField(max_length=255)        # Ombor nomi
    warehouse_lat = models.FloatField()                      # Latitude
    warehouse_lon = models.FloatField()                      # Longitude
    city_id = models.IntegerField()                          # Shahar ID
    city_name = models.CharField(max_length=100)             # Shahar nomi
    city_code = models.CharField(max_length=100)              # Shahar kodi
    region_name = models.CharField(max_length=100)           # Viloyat nomi
    index = models.CharField(max_length=20)                  # Indeks

    def __str__(self):
        return self.warehouse_name

    class Meta:
        ordering = ('id',)
        db_table = 'warehouse'
        indexes = [
            models.Index(fields=['id'])
        ]


class FullIndex(models.Model):
    index = models.CharField(max_length=20)
    region = models.CharField(max_length=100)
    geolocation = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ('id',)
        db_table = 'fullindex'
        indexes = [
            models.Index(fields=['id'])
        ]


class PostalOffice(models.Model):
    ems_international_post = models.CharField(max_length=500, null=True, blank=True)
    one_step = models.CharField(max_length=500, null=True, blank=True)
    index = models.CharField(max_length=200, null=True, blank=True)
    geolocation = models.TextField(null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    lat = models.CharField(max_length=200, null=True, blank=True)
    lng = models.CharField(max_length=200, null=True, blank=True)
    name_uz = models.CharField(max_length=500, null=True, blank=True)
    name_eng = models.CharField(max_length=500, null=True, blank=True)
    name_ru = models.CharField(max_length=500, null=True, blank=True)
    region = models.CharField(max_length=500, null=True, blank=True)
    city = models.CharField(max_length=500, null=True, blank=True)
    district = models.CharField(max_length=500, blank=True, null=True)
    mfy = models.CharField(max_length=500, null=True, blank=True)
    street = models.CharField(max_length=500, blank=True, null=True)
    village = models.CharField(max_length=500, blank=True, null=True)
    house = models.CharField(max_length=500, blank=True, null=True)
    apartment = models.CharField(max_length=500, blank=True, null=True)
    working_days = models.CharField(max_length=500, blank=True, null=True)
    working_days_2 = models.CharField(max_length=500, blank=True, null=True)
    working_hours = models.CharField(max_length=500, blank=True, null=True)
    working_hours_2 = models.CharField(max_length=500, blank=True, null=True)
    weekend_days = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ('id',)
        db_table = 'postaloffice'
        indexes = [
            models.Index(fields=['id'])
        ]

