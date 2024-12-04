from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status, filters
from models.models import CustomUser
from django.db.transaction import atomic
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework.throttling import UserRateThrottle
import requests
import time
from rest_framework.decorators import action
from django.contrib.auth.models import Group, Permission
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from zeep import Client
from zeep.helpers import serialize_object

from rest_framework_simplejwt.views import TokenObtainPairView
from core.middleware import static_token_required
from rest_framework.pagination import PageNumberPagination
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from .import_data import import_data
from .models import Warehouse
from .serializers import WarehouseSerializer


class ResultExelView(APIView):
    def get(self, request):
        data = import_data()
        return Response(data=data, status=status.HTTP_200_OK)


class IsCustomUsersPost(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'POST', 'OPTIONS'):
            return True
        return False

    def post(self, request):
        values = {
            "username": "+998505850551",
            "password": "Uzpost@9933",
            "remember_me": True
          }

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        # JSON formatida yuborish
        response = requests.post('https://prodapi.pochta.uz/api/v1/customer/authenticate', json=values, headers=headers)

        # Agar ma'lumotlar noto'g'ri bo'lsa, ma'lumotlar va statusni qaytarish
        # Agar hamma narsa to'g'ri bo'lsa
        data = response.json()
        if response.status_code != 200:
            return Response(data, status=response.status_code)
        return Response(data=data, status=status.HTTP_201_CREATED)


from pprint import pprint as p
import time
# Global token va muddati saqlanadigan o'zgaruvchilar


cached_token = None
token_expiry = 0


def gettoken():
    global cached_token, token_expiry
    # Token amal qilish muddati tugaganini tekshirish
    if cached_token and time.time() < token_expiry:
        return cached_token

    # Token olish uchun so'rov
    values = {
        "username": "+998505850551",
        "password": "Uzpost@9933",
        "remember_me": True
    }
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    response = requests.post('https://prodapi.pochta.uz/api/v1/customer/authenticate', json=values, headers=headers)

    data = response.json()
    if response.status_code != 200:
        return data["status"]

    # Yangi tokenni saqlash
    cached_token = data["data"]["id_token"]

    # Tokenning amal qilish muddati (odatda JWT tokenida "exp" maydoni bo'ladi)
    # Tokenning amal qilish vaqtini (24 soat yoki 86400 soniya) qo'shamiz
    token_expiry = time.time() + 86400

    return cached_token



class OrderServicesView(APIView):
    permission_classes = [IsCustomUsersPost, ]
    def get(self, request):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {gettoken()}'
        }
        data = {}
        request_1 = requests.get('https://prodapi.pochta.uz/api/v1/service_types', headers=headers)
        data_1 = request_1.json()
        if data_1["status"] == "success":
            data["service_types"] = data_1
        return Response(data=data, status=status.HTTP_200_OK)


class VIloyatuzbView(APIView):
    permission_classes = [IsCustomUsersPost, ]
    def get(self, request):
        data = {
            "Buxoro": "259",
            "Navoiy": "263",
            "Xorazm": "271",
            "Qoraqalpog'iston Respublikasi": "265",
            "Samarqand": "266",
            "Jizzax": "261",
            "Sirdaryo": "267",
            "Toshkent shahar": "270",
            "Toshkent viloyati": "269",
            "Andijon": "258",
            "Farg'ona": "260",
            "Namangan": "262",
            "Qashqadaryo": "264",
            "Surxondaryo": "268",
        }
        return Response(data=data, status=status.HTTP_200_OK)


class VIloyatkrlView(APIView):
    permission_classes = [IsCustomUsersPost]
    def get(self, request):
        data_k = {
            "Бухоро": "259",
            "Навоий": "263",
            "Хоразм": "271",
            "Қорақалпоғистон Республикаси": "265",
            "Самарқанд": "266",
            "Жиззах": "261",
            "Сирдарё": "267",
            "Тошкент шаҳар": "270",
            "Тошкент вилояти": "269",
            "Андижон": "258",
            "Фарғона": "260",
            "Наманган": "262",
            "Қашқадарё": "264",
            "Сурхондарё": "268",
        }
        return Response(data=data_k, status=status.HTTP_200_OK)


from transliterate import translit

# Lotin alifbosidagi qidiruvni kirillga o'tkazish funksiyasi
def to_cyrillic(text):
    try:
        return translit(text, 'ru')
    except:
        return text


class LocationsKrelUZbView(APIView):
    permission_classes = [IsCustomUsersPost, ]
    def get(self, request):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {gettoken()}'
        }
        parent_id = request.data.get('parent_id')
        if parent_id is None or type(parent_id) != int:
            return Response(data="Invalid parent_id", status=status.HTTP_400_BAD_REQUEST)
        data = {}
        request = requests.get('https://prodapi.pochta.uz/api/v2/jurisdiction/choose/list', headers=headers)
        data_2 = request.json()
        base = []
        if data_2["status"] == "success":
            for location in data_2["data"]:
                if location["parent_id"] == parent_id:
                    location["name"] = to_cyrillic(location["name"])
                    base.append(location)
        data_2["data"] = base
        data["locations"] = data_2
        return Response(data=data_2, status=status.HTTP_200_OK)


class LocationsUZbUZbView(APIView):
    permission_classes = [IsCustomUsersPost, ]
    def get(self, request):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {gettoken()}'
        }
        parent_id = request.data.get('parent_id')
        if parent_id is None or type(parent_id) != int:
            return Response(data="Invalid parent_id", status=status.HTTP_400_BAD_REQUEST)
        data = {}
        request = requests.get('https://prodapi.pochta.uz/api/v2/jurisdiction/choose/list', headers=headers)
        data_2 = request.json()
        base = []
        if data_2["status"] == "success":
            for location in data_2["data"]:
                if location["parent_id"] == parent_id:
                    base.append(location)
        data_2["data"] = base
        data["locations"] = data_2
        return Response(data=data_2, status=status.HTTP_200_OK)


class LocationsAllView(APIView):
    permission_classes = [IsCustomUsersPost]
    def get(self, request):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {gettoken()}'
        }
        data = {}
        request = requests.get('https://prodapi.pochta.uz/api/v2/jurisdiction/choose/list', headers=headers)
        data_2 = request.json()
        base = []
        if data_2["status"] == "success":
            for location in data_2["data"]:
                if len(location["hierarchy"]) == 0:
                    base.append(location)
        data_2["data"] = base
        return Response(data=data_2, status=status.HTTP_200_OK)


class LocationsKrelAllView(APIView):
    permission_classes = [IsCustomUsersPost]
    def get(self, request):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {gettoken()}'
        }
        data = {}
        request = requests.get('https://prodapi.pochta.uz/api/v2/jurisdiction/choose/list', headers=headers)
        data_2 = request.json()
        base = []
        if data_2["status"] == "success":
            for location in data_2["data"]:
                if len(location["hierarchy"]) == 0:
                    location["name"] = to_cyrillic(location["name"])
                    base.append(location)
        data_2["data"] = base
        return Response(data=data_2, status=status.HTTP_200_OK)


class CalculatorShipoxView(APIView):
    permission_classes = [IsCustomUsersPost, ]
    def get(self, request):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {gettoken()}'
        }
        data = {}
        weight = request.data.get("weight")
        if weight is None or type(weight) != float:
            return Response(data="vaznni raqam ko'rinishida kiritishga harakat qiling", status=status.HTTP_400_BAD_REQUEST)

        service_type_id = request.data.get("service_type_id")
        if service_type_id is None or type(service_type_id) != int:
            return Response(data="service_type_id int turida bo'lishi kerak", status=status.HTTP_400_BAD_REQUEST)

        fromjurisdiction_id = request.data.get("fromjurisdiction_id")
        if fromjurisdiction_id is None or type(fromjurisdiction_id) != int:
            return Response(data="fromjurisdiction_id int turida bo'lishi kerak", status=status.HTTP_400_BAD_REQUEST)

        tojurisdiction_id = request.data.get("tojurisdiction_id")
        if tojurisdiction_id is None or type(tojurisdiction_id) != int:
            return Response(data="tojurisdiction_id turida bo'lishi kerak")

        request = requests.get('https://prodapi.pochta.uz/api/v2/jurisdiction/choose/list', headers=headers)
        data_2 = request.json()
        from_latitude = ""
        from_longitude = ""
        to_latitude = ""
        to_longitude = ""
        fromJurisdictionId = None
        toJurisdictionId = None

        for i in data_2["data"]:
            if i["id"] == fromjurisdiction_id:
                fromJurisdictionId = fromjurisdiction_id
                from_latitude = i["lat"]
                from_longitude = i["lng"]
            if i["id"] == tojurisdiction_id:
                toJurisdictionId = tojurisdiction_id
                to_latitude = i["lat"]
                to_longitude = i["lng"]
        request = requests.get(f'https://prodapi.pochta.uz/api/v2/customer/packages/prices/starting_from?dimensions.weight={weight}&service_type={service_type_id}&page=0&size=20&fromJurisdictionId='
                               f'{fromJurisdictionId}&toJurisdictionId={toJurisdictionId}&from_latitude={from_latitude}&from_longitude={from_longitude}&to_latitude={to_latitude}&to_longitude={to_longitude}', headers=headers)
        request_x = requests.get(f"https://prodapi.pochta.uz/api/v2/customer/packages/prices/starting_from?dimensions.weight={weight}&service_type={service_type_id}&fromJurisdictionId={fromJurisdictionId}&toJurisdictionId={toJurisdictionId}", headers=headers)
        data = request.json()
        data_x = request_x.json()
        x = [data]
        return Response(data=x, status=status.HTTP_200_OK)


#@method_decorator(cache_page(60*1), name='dispatch')
class CalculatorShipoxIndexView(APIView):
    permission_classes = [IsCustomUsersPost, ]
    def get(self, request):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {gettoken()}'
        }
        data = {}
        weight = request.data.get("weight")
        if weight is None or type(weight) != float:
            return Response(data="vaznni raqam ko'rinishida kiritishga harakat qiling", status=status.HTTP_400_BAD_REQUEST)

        service_type_id = request.data.get("service_type_id")
        if service_type_id is None or type(service_type_id) != int:
            return Response(data="service_type_id int turida bo'lishi kerak", status=status.HTTP_400_BAD_REQUEST)

        fromjurisdiction_id = request.data.get("fromjurisdiction_id")
        if fromjurisdiction_id is None or type(fromjurisdiction_id) != int:
            return Response(data="fromjurisdiction_id int turida bo'lishi kerak", status=status.HTTP_400_BAD_REQUEST)

        tojurisdiction_id = request.data.get("index")
        if tojurisdiction_id is None:
            return Response(data="index ni kiritish kerak")
        warehouse = Warehouse.objects.filter(index=str(tojurisdiction_id)).first()
        request = requests.get('https://prodapi.pochta.uz/api/v2/jurisdiction/choose/list', headers=headers)
        data_2 = request.json()
        from_latitude = ""
        from_longitude = ""
        to_latitude = warehouse.warehouse_lat
        to_longitude = warehouse.warehouse_lon
        fromJurisdictionId = None
        toJurisdictionId = warehouse.city_id

        for i in data_2["data"]:
            if i["id"] == fromjurisdiction_id:
                fromJurisdictionId = fromjurisdiction_id
                from_latitude = i["lat"]
                from_longitude = i["lng"]
        request = requests.get(f'https://prodapi.pochta.uz/api/v2/customer/packages/prices/starting_from?dimensions.weight={weight}&service_type={service_type_id}&page=0&size=20&fromJurisdictionId='
                               f'{fromJurisdictionId}&toJurisdictionId={toJurisdictionId}&from_latitude={from_latitude}&from_longitude={from_longitude}&to_latitude={to_latitude}&to_longitude={to_longitude}', headers=headers)
        request_x = requests.get(f"https://prodapi.pochta.uz/api/v2/customer/packages/prices/starting_from?dimensions.weight={weight}&service_type={service_type_id}&fromJurisdictionId={fromJurisdictionId}&toJurisdictionId={toJurisdictionId}", headers=headers)
        data = request.json()
        data_x = request_x.json()
        x = [data]
        return Response(data=x, status=status.HTTP_200_OK)

# class Postindexfilter(filters.FilterSet):
#     warehouse_name = filters.CharFilter(field_name='warehouse_name', lookup_expr='icontains')
#     class Meta:
#         model = Warehouse
#         fields = ["warehouse_name"]


class PostIndexesView(APIView):
    permission_classes = [IsCustomUsersPost]

    def get(self, request):
        query = request.data.get('name')
        if query is None or type(query) != str:
            return Response(data="name is not correct", status=status.HTTP_400_BAD_REQUEST)
        query_x = to_cyrillic(query)
        data = Warehouse.objects.filter(warehouse_name__icontains=query_x)
        serializer = WarehouseSerializer(data, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)





















# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Warehouse
# import pandas as pd
# from rest_framework.parsers import MultiPartParser, FormParser
#
#
# class WarehouseImportView(APIView):
#     # Faylni olish uchun parser
#     parser_classes = (MultiPartParser, FormParser)
#
#     def post(self, request, *args, **kwargs):
#         # Faylni requestdan olish
#         file = request.FILES.get('file')
#
#         if not file:
#             return Response({"error": "Fayl kiritilmagan!"}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Excel faylini o'qing
#         try:
#             data = pd.read_excel(file)
#         except Exception as e:
#             return Response({"error": f"Faylni o'qishda xato: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
#
#         # Har bir qatordagi ma'lumotlarni saqlash
#         for _, row in data.iterrows():
#             Warehouse.objects.create(
#                 warehouse_id=row['warehouse_id'],
#                 warehouse_name=row['warehouse_name'],
#                 warehouse_lat=row['warehouse_lat'],
#                 warehouse_lon=row['warehouse_lon'],
#                 city_id=row['city_id'],
#                 city_name=row['city_name'],
#                 city_code=row['city_code'],
#                 region_name=row['region_name'],
#                 index=row['Index']
#             )
#
#         return Response({"message": "Ma'lumotlar muvaffaqiyatli saqlandi!"}, status=status.HTTP_201_CREATED)
#
#
#






