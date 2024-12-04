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
