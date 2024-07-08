from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
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


# Create your views here.
class ShipmentTrackingAPIView(APIView):
    permission_classes = [AllowAny, ]
    throttle_classes = [UserRateThrottle, ]

    def get(self, request):
        barcode = request.query_params.get('barcode')
        if not barcode:
            return Response({"error": "Barcode parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        data = requests.get(f"https://prodapi.pochta.uz/api/v1/public/order/{barcode}")
        data = data.json()
        if data["data"]['locations'][0]['country']['code'] == 'UZ' and data["data"]['locations'][0]['country']['code'] == 'UZ':
            total_data = requests.get(f"https://prodapi.pochta.uz/api/v1/public/order/{barcode}/history_items")
            return Response(data=total_data.json(), status=status.HTTP_200_OK)
        return Response({"error": "Barcode isn't valid."}, status=status.HTTP_404_NOT_FOUND)


class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', "POST", 'HEAD', 'OPTIONS'):
            return True
        return request.user.groups.filter(name='manager').exists()


class Tracking(APIView):
    permission_classes = [IsAuthenticated, ]
    throttle_classes = [UserRateThrottle, ]

    def get(self, request):
        barcode = request.query_params.get('barcode')
        if not barcode:
            return Response({"error": "Barcode parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        data = requests.get(f"https://prodapi.pochta.uz/api/v1/public/order/{barcode}")
        data = data.json()
        if data['status'] != "success":
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        if data["data"]['locations'][0]['country']['code'] == 'UZ' and data["data"]['locations'][0]['country']['code'] == 'UZ':
            total_data = requests.get(f"https://prodapi.pochta.uz/api/v1/public/order/{barcode}/history_items")
            return Response(data=total_data.json(), status=status.HTTP_200_OK)

        url1 = f"https://gdeposylka.ru/api/v4/tracker/detect/{barcode}"
        headers = {
            "X-Authorization-Token": "65bbbac85f796f8032e0874411f4d1f5af7185a99e184709bf0c1f38d95486fa2338733760a48704"
        }
        response1 = requests.get(url1, headers=headers)
        data = response1.json()
        total_data = []
        for item in data['data']:
            url2 = f"https://gdeposylka.ru/api/v4/tracker/{item['courier']['slug']}/{barcode}"
            response2 = requests.get(url2, headers=headers)
            response_x = response2.json()
            if len(response_x["messages"]) == 0:
                total_data.append(response2.json())
            else:
                time.sleep(15)
                response2 = requests.get(url2, headers=headers)
                total_data.append(response2.json())
        return Response(total_data, status=status.HTTP_200_OK)

