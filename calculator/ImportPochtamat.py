import pandas as pd
from .models import Warehouse, PostalOffice, FullIndex
import json


def ImportPostalOffice():
    # Excel fayl yo'lini ko'rsatish
    file_path = "D:/lessons/Uzpost_Porject/django_project_uzpost/calculator/postal_offices.json"
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Ma'lumotlarni o'qish va database'ga saqlash
    for row in data.keys():
        if row == "Full Indexes":
            for column in data[row]:
                FullIndex.objects.create(
                    index=column["Индекс"],
                    region=column["Город\n(Область)"],
                    geolocation=column.get("Геолокация (Яндекс Карты или GoogleMaps)") if column.get("Геолокация (Яндекс Карты или GoogleMaps)") else None,
                    comments=column.get('Комментарии') if column.get('Комментарии') else None
                    )
        for row in data[row]:
            print(row.get("EMS"))
            ems_international_post = row.get('EMS') if row.get(
                'EMS') else None
            one_step = row.get('Bir Qadam') if row.get('Bir Qadam') else None
            index = row.get('Индекс') if row.get("Индекс") else None
            geolocation = row.get('Геолокация (Яндекс Карты или GoogleMaps)', None)
            comments = row.get('Комментарии') if row.get('Комментарии') else None
            lat = row.get('LAT') if row.get('LAT') else None
            lng = row.get('LNG') if row.get('LNG') else None
            name_uz = row.get('name_uz') if row.get('name_uz') else None
            name_eng = row.get('name_english') if row.get('name_english') else None
            name_ru = row.get('name_rus') if row.get('name_rus') else None
            region = row.get('Область') if row.get('Область') else None
            city = row.get('Город') if row.get('Город') else None
            district = row.get('Район') if row.get('Район') else None
            mfy = row.get('МФЙ') if row.get('МФЙ') else None
            street = row.get('Улица') if row.get('Улица') else None
            village = row.get('Кишлак') if row.get('Кишлак') else None
            house = row.get('Дом') if row.get('Дом') else None
            apartment = row.get('Квартира') if row.get('Квартира') else None
            working_days = row.get('Дни работы') if row.get('Дни работы') else None
            working_days_2 = row.get('Дни работы 2') if row.get('Дни работы 2') else None
            working_hours = row.get('Время работы') if row.get('Время работы') else None
            working_hours_2 = row.get('Время работы 2') if row.get('Время работы 2') else None
            weekend_days = row.get('Выходные') if row.get('Выходные') else None

            # PostalOffice modeliga saqlash
            PostalOffice.objects.create(
                ems_international_post=ems_international_post,
                one_step=one_step,
                index=index,
                geolocation=geolocation,
                comments=comments,
                lat=lat,
                lng=lng,
                name_uz=name_uz,
                name_eng=name_eng,
                name_ru=name_ru,
                region=region,
                city=city,
                district=district,
                mfy=mfy,
                street=street,
                village=village,
                house=house,
                apartment=apartment,
                working_days=working_days,
                working_days_2=working_days_2,
                working_hours=working_hours,
                working_hours_2=working_hours_2,
                weekend_days=weekend_days,
            )

    return "Excel fayldan ma'lumotlar muvaffaqiyatli import qilindi!"