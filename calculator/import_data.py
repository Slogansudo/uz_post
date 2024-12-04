import pandas as pd
from .models import Warehouse


def import_data():
# Excel faylini o'qing
    file_path = "D:/lessons/Uzpost_Porject/django_project_uzpost/calculator/warehouses_branch_active_20240912.xlsx"
    data = pd.read_excel(file_path)

    for _, row in data.iterrows():
        Warehouse.objects.create(
            warehouse_name=row['warehouse_name'],
            warehouse_lat=row['warehouse_lat'],
            warehouse_lon=row['warehouse_lon'],
            city_id=row['city_id'],
            city_name=row['city_name'],
            city_code=row['city_code'],
            region_name=row['region_name'],
            index=row['Index']
        )
    return "Ma'lumotlar muvaffaqiyatli saqlandi!"
