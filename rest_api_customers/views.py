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

# new
from models.models import (CustomUser, UsersRequests, IPAddressLog)
from db_models.models import (Banners, MenuElements, Menu, StatisticItems, Statistics, TegRegions, TegWorkingDays,
                              TegExperience, TegVacancies, TegBranches2, Vacancies, Purchases, Marks, SaveMediaFiles,
                              Events, UzPostNews, PostalServices, Pages, BranchServices, ShablonServices, Branches,
                              VacanciesImages, InternalDocuments, ThemaQuestions, BusinessPlansCompleted, AnnualReports,
                              Dividends, QuarterReports, UserInstructions, ExecutiveApparatus, ShablonUzPostTelNumber,
                              ShablonContactSpecialTitle, Contact, Advertisements, OrganicManagements, Partners,
                              RegionalBranches, Advertising, InformationAboutIssuer, Slides, SocialMedia, EssentialFacts,
                              Rates, Services, CharterSociety, SecurityPapers, FAQ, SiteSettings, CategoryPages, ControlCategoryPages)

from rest_api.serializes import (UsersRequestsSerializer, BannersSerializer, MenuElementsSerializer,
                        MenuSerializer, StatisticItemsSerializer, StatisticsSerializer, TegRegionsSerializer,
                        TegWorkingDaysSerializer, TegExperiencesSerializer, TegVacanciesSerializer, TegBranches2Serializer,
                        VacanciesSerializer, PurchasesSerializer, MarksSerializer, SaveMediaFilesSerializer, EventsSerializer,
                         UzPostNewsSerializer, PostalServicesSerializer, PagesSerializer, BranchServicesSerializer,
                         ShablonServicesSerializer, BranchesSerializer, VacanciesImagesSerializer, InternalDocumentsSerializer,
                         ThemaQuestionsSerializer, BusinessPlansCompletedSerializer, AnnualReportsSerializer, DividendsSerializer,
                         QuarterReportsSerializer, UserInstructionsSerializer, ExecutiveApparatusSerializer, ShablonUzPostTelNumberSerializer, ShablonContactSpecialTitleSerializer,
                         ContactSerializer, AdvertisementsSerializer, OrganicManagementsSerializer, PartnersSerializer, RegionalBranchesSerializer,
                         AdvertisingSerializer, InformationAboutIssuerSerializer, SlidesSerializer, SocialMediaSerializer, EssentialFactsSerializer,
                         RatesSerializer, ServicesSerializer, CharterSocietySerializer, SecurityPapersSerializer, FAQSerializer,
                         SiteSettingsSerializer, CategoryPagesSerializer, ControlCategoryPagesSerializer)
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from zeep import Client
from zeep.helpers import serialize_object


class CustomUserThrottle(UserRateThrottle):
    rate = '30/minute'


class CustomUserUnauthorizedThrottle(UserRateThrottle):
    rate = '15/minute'


class IsCustomUsersGet(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'OPTIONS'):
            return True
        return False


class IsCustomUsersPost(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'POST', 'OPTIONS'):
            return True
        return False


class RegisterUserView(APIView):
    permission_classes = [AllowAny, ]
    throttle_classes = [CustomUserUnauthorizedThrottle, ]

    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response(data="No phone number provided", status=status.HTTP_400_BAD_REQUEST)
        if type(phone_number) != str:
            return Response(data="phone number is type invalid it is type str", status=status.HTTP_400_BAD_REQUEST)
        if len(phone_number) != 9:
            return Response(data="phone number should not exceed 9 characters", status=status.HTTP_400_BAD_REQUEST)
        phone_number = f"+998{phone_number}"
        custom_user = CustomUser.objects.filter(phone_number=phone_number).first()
        if custom_user:
            return Response('custom user with this phone number already exists.', status=status.HTTP_400_BAD_REQUEST)
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        image = request.data.get('image')
        region = request.data.get('region')
        district = request.data.get('district')
        if not first_name:
            first_name = None
        if not last_name:
            last_name = None
        if not image:
            image = None
        if not region:
            region = None
        if not district:
            district = None

        password = request.data.get('password')
        if not password:
            return Response(data="Password must be entered", status=status.HTTP_400_BAD_REQUEST)
        if type(password) != str:
            return Response(data="password is type invalid it is type str", status=status.HTTP_400_BAD_REQUEST)
        if len(password) < 6:
            return Response('password must be longer than 6 characters', status=status.HTTP_400_BAD_REQUEST)

        custom_user = CustomUser(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            image=image,
            region=region,
            district=district,
            password=make_password(password)  # Parolni hashlash

        )
        custom_user.save()

        return Response('successful registration', status=status.HTTP_201_CREATED)


class MyProfileView(APIView):
     permission_classes = [IsAuthenticated, ]
     throttle_classes = [CustomUserThrottle, ]

     def get(self, request):
         user = CustomUser.objects.filter(phone_number=request.user.phone_number).first()
         data = {
             "phone_number": user.phone_number,
             'first_name': user.first_name,
             'last_name': user.last_name,
             'image': user.image.url if user.image else None,
             'region': user.region,
             'district': user.district,
             'password': "********"
         }
         return Response(data, status=status.HTTP_200_OK)

     def put(self, request):
         user = CustomUser.objects.filter(phone_number=request.user.phone_number).first()
         if not user:
             return Response("User not found", status=status.HTTP_404_NOT_FOUND)

         data = request.data
         first_name = data.get('first_name')
         last_name = data.get('last_name')
         image = request.FILES.get('image')
         remove_image = data.get('remove_image')  # Rasmni o'chirish uchun bayroq
         region = data.get('region')
         district = data.get('district')
         password = data.get('password')

         if not password:
             return Response("Password must be entered", status=status.HTTP_400_BAD_REQUEST)
         if len(password) < 6:
             return Response('Password must be longer than 6 characters', status=status.HTTP_400_BAD_REQUEST)

         user.first_name = first_name if first_name else user.first_name
         user.last_name = last_name if last_name else user.last_name
         if image:
             if user.image:
                user.image.delete()
             user.image = image  # Agar yangi rasm berilgan bo'lsa, yangilash
         elif remove_image:
             user.image.delete()  # Rasmni o'chirish
             user.image = None
         user.region = region if region else user.region
         user.district = district if district else user.district
         user.password = make_password(password)
         user.save()

         data = {
             "phone_number": user.phone_number,
             'first_name': user.first_name,
             'last_name': user.last_name,
             'image': user.image.url if user.image else None,  # URL yoki None
             'region': user.region,
             'district': user.district,
             'password': "********"
         }
         return Response(data, status=status.HTTP_200_OK)

     def delete(self, request):
         user = CustomUser.objects.filter(phone_number=request.user.phone_number).first()
         user.is_active = False
         user.save()
         return Response(data='successful deleted', status=status.HTTP_204_NO_CONTENT)


@method_decorator(cache_page(60*15), name='dispatch')
class Barcode(APIView):
    permission_classes = [AllowAny, ]
    throttle_classes = [CustomUserUnauthorizedThrottle, ]

    def get(self, request, barcode):
        if barcode[:2] == "RZ" or barcode[:2] == "CZ" or barcode[:1] == "E":
            wsdl = 'http://10.100.0.69/IPSAPIService/TrackAndTraceService.svc?singleWsdl'

            # SOAP servisi uchun ulanish
            client = Client(wsdl=wsdl)

            # Parametrlar tayyorlash
            ids = barcode
            # lang = 'RU'
            token = '269a208f-7006-4dc6-b52f-6dfba6af113a'

            # GetMailitems metodini chaqirish
            response = client.service.GetMailitems(ids=ids, token=token)

            # SOAP javobini dictionary'ga aylantirish
            response_data = serialize_object(response)
            if response_data == None:
                first = {
                    "code": "order_not_found",
                    "message": "Order Not Found",
                    "request_id": "69f059d0-1748-42cc-982c-7a322c4e81fa",
                    "status": "error"
                }
                return Response(data=first, status=status.HTTP_404_NOT_FOUND)
            response_data_2 = response_data
            if response_data_2[0]["InfoFromEdi"] != None:
                for i in range(len(
                        response_data_2[0]["InfoFromEdi"]["TMailitemInfoFromEDI"][0]["Events"]["TMailitemEventEDI"])):
                    response_data_2[0]["InfoFromEdi"]["TMailitemInfoFromEDI"][0]["Events"]["TMailitemEventEDI"][i][
                        "ReceivedDispatch"] = None
            if response_data_2[0]["OperationalMailitems"] != None:
                for j in range(len(response_data_2[0]["OperationalMailitems"]["TMailitemInfoFromScanning"][0]["Events"][
                                       "TMailitemEventScanning"])):
                    response_data_2[0]["OperationalMailitems"]["TMailitemInfoFromScanning"][0]["Events"][
                        "TMailitemEventScanning"][j]["ReceivedDispatch"] = None
            return Response(data=response_data_2, status=status.HTTP_200_OK)


        data = requests.get(f"https://prodapi.pochta.uz/api/v1/public/order/{barcode}")
        data = data.json()
        if data['status'] != "success":
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        total_data_2 = {'header': data}
        if barcode[:2] != 'SX' and data["data"]['locations'][0]['country']['code'] == 'UZ' and data["data"]['locations'][1]['country']['code'] == 'UZ':
            total_data = requests.get(f"https://prodapi.pochta.uz/api/v1/public/order/{barcode}/history_items")
            total_data_2['shipox'] = total_data.json()
            total_data_2['gdeposilka'] = None
            return Response(total_data_2, status=status.HTTP_200_OK)

        url1 = f"https://gdeposylka.ru/api/v4/tracker/detect/{barcode}"
        headers = {
            "X-Authorization-Token": "65bbbac85f796f8032e0874411f4d1f5af7185a99e184709bf0c1f38d95486fa2338733760a48704"
        }
        response1 = requests.get(url1, headers=headers)
        data = response1.json()
        shipox = requests.get(f"https://prodapi.pochta.uz/api/v1/public/order/{barcode}/history_items")
        total_data_2['shipox'] = shipox.json()

        url2 = f"https://gdeposylka.ru{data['data'][0]['tracker_url']}"
        response2 = requests.get(url2, headers=headers)
        response_x = response2.json()
        if len(response_x["messages"]) == 0:
            gdeposylka = {
                "result": response_x['result'],
                'data': {
                    'id': response_x['data']['id'],
                    'tracking_number': response_x['data']['tracking_number'],
                    "tracking_number_secondary": response_x['data']['tracking_number_secondary'],
                    "tracking_number_current": response_x['data']['tracking_number_current'],
                    "courier": response_x['data']['courier'],
                    "is_active": response_x['data']['is_active'],
                    "is_delivered": response_x['data']['is_delivered'],
                    "last_check": response_x['data']['last_check'],
                    'checkpoints': [],
                    "extra": response_x['data']['extra']
                }
            }
            for points in response_x['data']['checkpoints']:
                if points['courier']['slug'] != 'ozbekiston-pochtasi':
                    gdeposylka['data']['checkpoints'].append(points)
            total_data_2['gdeposilka'] = gdeposylka
        else:
            time.sleep(15)
            response2 = requests.get(url2, headers=headers)
            response_x = response2.json()
            if len(response_x['messages']) == 0:
                gdeposylka = {
                    "result": response_x['result'],
                    'data': {
                        'id': response_x['data']['id'],
                        'tracking_number': response_x['data']['tracking_number'],
                        "tracking_number_secondary": response_x['data']['tracking_number_secondary'],
                        "tracking_number_current": response_x['data']['tracking_number_current'],
                        "courier": response_x['data']['courier'],
                        "is_active": response_x['data']['is_active'],
                        "is_delivered": response_x['data']['is_delivered'],
                        "last_check": response_x['data']['last_check'],
                        'checkpoints': [],
                        "extra": response_x['data']['extra']
                    }
                }
                for points in response_x['data']['checkpoints']:
                    if points['courier']['slug'] != 'ozbekiston-pochtasi':
                        gdeposylka['data']['checkpoints'].append(points)
                total_data_2['gdeposilka'] = gdeposylka
            else:
                total_data_2['gdeposilka'] = "please try again we are processing the data"
        return Response(total_data_2, status=status.HTTP_200_OK)


@method_decorator(cache_page(60*15), name='dispatch')
class TrackIsAuth(APIView):
    permission_classes = [IsAuthenticated, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def get(self, request, barcode):
        if barcode[:2] == "RZ" or barcode[:2] == "CZ" or barcode[:1] == "E":
            wsdl = 'http://10.100.0.69/IPSAPIService/TrackAndTraceService.svc?singleWsdl'

            # SOAP servisi uchun ulanish
            client = Client(wsdl=wsdl)

            # Parametrlar tayyorlash
            ids = barcode
            # lang = 'RU'
            token = '269a208f-7006-4dc6-b52f-6dfba6af113a'

            # GetMailitems metodini chaqirish
            response = client.service.GetMailitems(ids=ids, token=token)

            # SOAP javobini dictionary'ga aylantirish
            response_data = serialize_object(response)
            if response_data == None:
                first = {
	            "code": "order_not_found",
	            "message": "Order Not Found",
	            "request_id": "69f059d0-1748-42cc-982c-7a322c4e81fa",
	            "status": "error"
                }
                return Response(data=first, status=status.HTTP_404_NOT_FOUND)
            response_data_2 = response_data
            if response_data_2[0]["InfoFromEdi"] != None:
                for i in range(len(response_data_2[0]["InfoFromEdi"]["TMailitemInfoFromEDI"][0]["Events"]["TMailitemEventEDI"])):
                    response_data_2[0]["InfoFromEdi"]["TMailitemInfoFromEDI"][0]["Events"]["TMailitemEventEDI"][i]["ReceivedDispatch"] = None
            if response_data_2[0]["OperationalMailitems"] != None:
                for j in range(len(response_data_2[0]["OperationalMailitems"]["TMailitemInfoFromScanning"][0]["Events"]["TMailitemEventScanning"])):
                    response_data_2[0]["OperationalMailitems"]["TMailitemInfoFromScanning"][0]["Events"]["TMailitemEventScanning"][j]["ReceivedDispatch"] = None
            return Response(data=response_data_2, status=status.HTTP_200_OK)


        data = requests.get(f"https://prodapi.pochta.uz/api/v1/public/order/{barcode}")
        data = data.json()
        if data['status'] != "success":
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        total_data_2 = {'header': data}
        if barcode[:2] != 'SX' and data["data"]['locations'][0]['country']['code'] == 'UZ' and data["data"]['locations'][1]['country']['code'] == 'UZ':
            total_data = requests.get(f"https://prodapi.pochta.uz/api/v1/public/order/{barcode}/history_items")
            total_data_2['shipox'] = total_data.json()
            total_data_2['gdeposilka'] = None
            return Response(total_data_2, status=status.HTTP_200_OK)
        url1 = f"https://gdeposylka.ru/api/v4/tracker/detect/{barcode}"
        headers = {
            "X-Authorization-Token": "65bbbac85f796f8032e0874411f4d1f5af7185a99e184709bf0c1f38d95486fa2338733760a48704"
        }
        response1 = requests.get(url1, headers=headers)
        data = response1.json()
        shipox = requests.get(f"https://prodapi.pochta.uz/api/v1/public/order/{barcode}/history_items")
        total_data_2['shipox'] = shipox.json()

        url2 = f"https://gdeposylka.ru{data['data'][0]['tracker_url']}"
        response2 = requests.get(url2, headers=headers)
        response_x = response2.json()
        if len(response_x["messages"]) == 0:
            gdeposylka = {
                "result": response_x['result'],
                'data': {
                    'id': response_x['data']['id'],
                    'tracking_number': response_x['data']['tracking_number'],
                    "tracking_number_secondary": response_x['data']['tracking_number_secondary'],
                    "tracking_number_current": response_x['data']['tracking_number_current'],
                    "courier": response_x['data']['courier'],
                    "is_active": response_x['data']['is_active'],
                    "is_delivered": response_x['data']['is_delivered'],
                    "last_check": response_x['data']['last_check'],
                    'checkpoints': [],
                    "extra": response_x['data']['extra']
                }
            }
            for points in response_x['data']['checkpoints']:
                if points['courier']['slug'] != 'ozbekiston-pochtasi':
                    gdeposylka['data']['checkpoints'].append(points)
            total_data_2['gdeposilka'] = gdeposylka
        else:
            time.sleep(15)
            response2 = requests.get(url2, headers=headers)
            response_x = response2.json()
            if len(response_x['messages']) == 0:
                gdeposylka = {
                    "result": response_x['result'],
                    'data': {
                        'id': response_x['data']['id'],
                        'tracking_number': response_x['data']['tracking_number'],
                        "tracking_number_secondary": response_x['data']['tracking_number_secondary'],
                        "tracking_number_current": response_x['data']['tracking_number_current'],
                        "courier": response_x['data']['courier'],
                        "is_active": response_x['data']['is_active'],
                        "is_delivered": response_x['data']['is_delivered'],
                        "last_check": response_x['data']['last_check'],
                        'checkpoints': [],
                        "extra": response_x['data']['extra']
                    }
                }
                for points in response_x['data']['checkpoints']:
                    if points['courier']['slug'] != 'ozbekiston-pochtasi':
                        gdeposylka['data']['checkpoints'].append(points)
                total_data_2['gdeposilka'] = gdeposylka
            else:
                total_data_2['gdeposilka'] = "please try again we are processing the data"
        return Response(data=total_data_2, status=status.HTTP_200_OK)


@method_decorator(cache_page(60*15), name='dispatch')
class TmuTrackAPIView(APIView):
    permission_classes = [IsAuthenticated, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def get(self, request, barcode):
        if barcode[:2] == "RZ" or barcode[:2] == "CZ" or barcode[:1] == "E":
            wsdl = 'http://10.100.0.69/IPSAPIService/TrackAndTraceService.svc?singleWsdl'

            # SOAP servisi uchun ulanish
            client = Client(wsdl=wsdl)

            # Parametrlar tayyorlash
            ids = barcode
            # lang = 'RU'
            token = '269a208f-7006-4dc6-b52f-6dfba6af113a'

            # GetMailitems metodini chaqirish
            response = client.service.GetMailitems(ids=ids, token=token)

            # SOAP javobini dictionary'ga aylantirish
            response_data = serialize_object(response)
            if response_data == None:
                first = {
                    "code": "order_not_found",
                    "message": "Order Not Found",
                    "request_id": "69f059d0-1748-42cc-982c-7a322c4e81fa",
                    "status": "error"
                }
                return Response(data=first, status=status.HTTP_404_NOT_FOUND)
            response_data_2 = response_data
            if response_data_2[0]["InfoFromEdi"] != None:
                for i in range(len(
                        response_data_2[0]["InfoFromEdi"]["TMailitemInfoFromEDI"][0]["Events"]["TMailitemEventEDI"])):
                    response_data_2[0]["InfoFromEdi"]["TMailitemInfoFromEDI"][0]["Events"]["TMailitemEventEDI"][i][
                        "ReceivedDispatch"] = None
            if response_data_2[0]["OperationalMailitems"] != None:
                for j in range(len(response_data_2[0]["OperationalMailitems"]["TMailitemInfoFromScanning"][0]["Events"][
                                       "TMailitemEventScanning"])):
                    response_data_2[0]["OperationalMailitems"]["TMailitemInfoFromScanning"][0]["Events"][
                        "TMailitemEventScanning"][j]["ReceivedDispatch"] = None
            return Response(data=response_data_2, status=status.HTTP_200_OK)
        first = {
            "code": "order_not_found",
            "message": "Order Not Found",
            "request_id": "69f059d0-1748-42cc-982c-7a322c4e81fa",
            "status": "error"
        }
        return Response(data=first, status=status.HTTP_404_NOT_FOUND)


class UsersRequestsDetailView(APIView):
    permission_classes = [AllowAny, IsCustomUsersPost]
    throttle_classes = [CustomUserThrottle, ]

    def post(self, request):
        serializer = UsersRequestsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BannerAPIViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    queryset = Banners.objects.all()
    serializer_class = BannersSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.image:
            if os.path.isfile(instance.image.path):
                os.remove(instance.image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'image' in request.data and not request.data['image']:
            if instance.image:
                if os.path.isfile(instance.image.path):
                    os.remove(instance.image.path)
                instance.image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class MenuElementsAPIViewSet(viewsets.ModelViewSet):
    queryset = MenuElements.objects.all()
    serializer_class = MenuElementsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]


class MenuAPIViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    @action(detail=True, methods=['get'])
    def menu_elements(self, request, *args, **kwargs):
        menu = self.get_object()
        menu_elements = menu.menu_elements.all()
        serializer = MenuElementsSerializer(menu_elements, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @menu_elements.mapping.post
    def add_menu_element(self, request, *args, **kwargs):
        menu = self.get_object()
        serializer = MenuElementsSerializer(data=request.data)
        if serializer.is_valid():
            menu_element = serializer.save()
            menu.menu_elements.add(menu_element)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def menu_element_detail(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        menu = self.get_object()
        menu_elements = menu.menu_elements.filter(id=id).first()
        if menu_elements is None:
            return Response(data="Statistic Item not found", status=status.HTTP_404_NOT_FOUND)
        serializer = MenuElementsSerializer(menu_elements)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @menu_element_detail.mapping.put
    def update_menu_element_detail(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        menu = self.get_object()
        menu_elements = menu.menu_elements.filter(id=id).first()
        if menu_elements is None:
            return Response(data="Menu Element not found", status=status.HTTP_404_NOT_FOUND)
        serializer = MenuElementsSerializer(menu_elements, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @menu_element_detail.mapping.delete
    def delete_menu_element(self, request, *args, **kwargs):
        menu = self.get_object()
        id = request.data.get('id')
        if type(id) != int:
            return Response(data="You must enter the id as an int type", status=status.HTTP_400_BAD_REQUEST)
        data = menu.menu_elements.filter(id=id)
        if not data:
            return Response(data="No such menu element", status=status.HTTP_404_NOT_FOUND)
        menu.menu_elements.remove(data.first())
        menu_elements = MenuElements.objects.get(id=id)
        menu_elements.delete()
        return Response(data="successful deleted", status=status.HTTP_204_NO_CONTENT)


class StatisticItemsAPIViewSet(viewsets.ModelViewSet):
    queryset = StatisticItems.objects.all()
    serializer_class = StatisticItemsSerializer
    permission_classes = [AllowAny, IsCustomUsersPost]
    throttle_classes = [CustomUserThrottle, ]

    @action(detail=False, methods=['POST'])
    def item_score(self, request, *args, **kwargs):
        id = request.data.get('id')
        if not id:
            return Response(data="No such id", status=status.HTTP_400_BAD_REQUEST)
        try:
            id = int(id)
        except ValueError:
            return Response(data="You must enter the id as int type", status=status.HTTP_400_BAD_REQUEST)

        data = get_object_or_404(StatisticItems, id=id)
        data.number_responses += 1
        data.save()
        return Response(data="successful", status=status.HTTP_200_OK)


class StatisticsAPIViewSet(viewsets.ModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    @action(detail=True, methods=['get'])
    def statistic_items(self, request, *args, **kwargs):
        statistic = self.get_object()
        statistic_items = statistic.statistic_items.all()
        serializer = StatisticItemsSerializer(statistic_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @statistic_items.mapping.post
    def add_statistic_item(self, request, *args, **kwargs):
        statistics = self.get_object()
        serializer = StatisticItemsSerializer(data=request.data)
        if serializer.is_valid():
            statistic_item = serializer.save()
            statistics.statistic_items.add(statistic_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def statistic_item_detail(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        statistic = self.get_object()
        statistic_items = statistic.statistic_items.filter(id=id).first()
        if statistic_items is None:
            return Response(data="Statistic Item not found", status=status.HTTP_404_NOT_FOUND)
        serializer = StatisticItemsSerializer(statistic_items)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @statistic_item_detail.mapping.put
    def update_statistic_item(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        statistic = self.get_object()
        statistic_item = statistic.statistic_items.filter(id=id).first()
        if statistic_item is None:
            return Response(data="Statistic Item not found", status=status.HTTP_404_NOT_FOUND)
        serializer = StatisticItemsSerializer(statistic_item, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @statistic_item_detail.mapping.delete
    def delete_statistic_item(self, request, *args, **kwargs):
        statistics = self.get_object()
        id = request.data.get('id')
        if type(id) != int:
            return Response(data="You must enter the id as an int type", status=status.HTTP_400_BAD_REQUEST)
        data = statistics.statistic_items.filter(id=id)
        if not data:
            return Response(data="No such menu element", status=status.HTTP_404_NOT_FOUND)
        statistics.statistic_items.remove(data.first())
        statistic_items = StatisticItems.objects.get(id=id)
        statistic_items.delete()
        return Response(data="successful deleted", status=status.HTTP_204_NO_CONTENT)


class TegRegionsAPIViewSet(viewsets.ModelViewSet):
    queryset = TegRegions.objects.all()
    serializer_class = TegRegionsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]


class TegWorkingDaysAPIViewSet(viewsets.ModelViewSet):
    queryset = TegWorkingDays.objects.all()
    serializer_class = TegWorkingDaysSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]


class TegExperiencesAPIViewSet(viewsets.ModelViewSet):
    queryset = TegExperience.objects.all()
    serializer_class = TegExperiencesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]


class TegVacanciesAPIViewSet(viewsets.ModelViewSet):
    queryset = TegVacancies.objects.all()
    serializer_class = TegVacanciesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]


class TegBranches2APIViewSet(viewsets.ModelViewSet):
    queryset = TegBranches2.objects.all()
    serializer_class = TegBranches2Serializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]


class VacanciesAPIViewSet(viewsets.ModelViewSet):
    queryset = Vacancies.objects.all()
    serializer_class = VacanciesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class PurchasesAPIViewSet(ModelViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class MarksAPIViewSet(ModelViewSet):
    queryset = Marks.objects.all()
    serializer_class = MarksSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class SaveMediaFilesAPIViewSet(ModelViewSet):
    queryset = SaveMediaFiles.objects.all()
    serializer_class = SaveMediaFilesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.file:
            if os.path.isfile(instance.file.path):
                os.remove(instance.file.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'file' in request.data and not request.data['file']:
            if instance.file:
                if os.path.isfile(instance.file.path):
                    os.remove(instance.file.path)
                instance.file = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class EventsAPIViewSet(ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class UzPostNewsAPIViewSet(ModelViewSet):
    queryset = UzPostNews.objects.all()
    serializer_class = UzPostNewsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class PostalServicesAPIViewSet(ModelViewSet):
    queryset = PostalServices.objects.all()
    serializer_class = PostalServicesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class PagesAPIViewSet(ModelViewSet):
    queryset = Pages.objects.all()
    serializer_class = PagesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class CategoryPagesViewSet(ModelViewSet):
    queryset = CategoryPages.objects.all()
    serializer_class = CategoryPagesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    @action(detail=True, methods=['post'])
    def pages(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = PagesSerializer(data=request.data)
        if serializer.is_valid():
            pages = serializer.save()
            category.pages.add(pages)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @pages.mapping.put
    def update_pages(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        category = self.get_object()
        page = category.pages.filter(id=id).first()
        if page is None:
            return Response(data="postal service not found", status=status.HTTP_404_NOT_FOUND)
        serializer = PagesSerializer(page, data=request.data)
        if serializer.is_valid():
            page_1 = serializer.save()
            page_1.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @pages.mapping.delete
    def delete_pages(self, request, *args, **kwargs):
        category = self.get_object()
        id = request.data.get('id')
        if type(id) != int:
            return Response(data="You must enter the id as an int type", status=status.HTTP_400_BAD_REQUEST)
        data = category.pages.filter(id=id)
        if not data:
            return Response(data="No such postal service", status=status.HTTP_404_NOT_FOUND)
        category.pages.remove(data.first())
        page = Pages.objects.get(id=id)
        page.delete()
        return Response(data="successful deleted", status=status.HTTP_204_NO_CONTENT)


class ControlCategoryPageViewSet(ModelViewSet):
    queryset = ControlCategoryPages.objects.all()
    serializer_class = ControlCategoryPagesSerializer
    permission_classes = [IsAuthenticated, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    @action(detail=True, methods=['post'])
    def category_pages(self, request, *args, **kwargs):
        control_category = self.get_object()
        serializer = CategoryPagesSerializer(data=request.data)
        if serializer.is_valid():
            category = serializer.save()
            control_category.page_categories.add(category)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @category_pages.mapping.put
    def update_category_page(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        control_category_page = self.get_object()
        page = control_category_page.page_categories.filter(id=id).first()
        if page is None:
            return Response(data="category page not found", status=status.HTTP_404_NOT_FOUND)
        serializer = CategoryPagesSerializer(page, data=request.data)
        if serializer.is_valid():
            page_1 = serializer.save()
            page_1.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @category_pages.mapping.delete
    def delete_category_page(self, request, *args, **kwargs):
        controlcategory = self.get_object()
        id = request.data.get('id')
        if type(id) != int:
            return Response(data="You must enter the id as an int type", status=status.HTTP_400_BAD_REQUEST)
        data = controlcategory.page_categories.filter(id=id)
        if not data:
            return Response(data="No such category pages", status=status.HTTP_404_NOT_FOUND)
        controlcategory.page_categories.remove(data.first())
        category_page = CategoryPages.objects.get(id=id)
        category_page.delete()
        return Response(data="successful deleted", status=status.HTTP_204_NO_CONTENT)


class BranchServicesAPIViewSet(ModelViewSet):
    queryset = BranchServices.objects.all()
    serializer_class = BranchServicesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class ShablonServicesAPIViewSet(ModelViewSet):
    queryset = ShablonServices.objects.all()
    serializer_class = ShablonServicesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]



class BranchesAPIViewSet(ModelViewSet):
    queryset = Branches.objects.all()
    serializer_class = BranchesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
    """
    servise yani usluga qo'shib o'chirish uchun kerak bo'lgan actionlar
    """
    @action(detail=True, methods=['post'])
    def postal_service(self, request, *args, **kwargs):
        branch = self.get_object()
        serializer = ShablonServicesSerializer(data=request.data)
        if serializer.is_valid():
            postal_service = serializer.save()
            branch.postal_service.add(postal_service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @postal_service.mapping.put
    def update_postal_service(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        branch = self.get_object()
        postal_service = branch.postal_service.filter(id=id).first()
        if postal_service is None:
            return Response(data="postal service not found", status=status.HTTP_404_NOT_FOUND)
        serializer = ShablonServicesSerializer(postal_service, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @postal_service.mapping.delete
    def delete_postal_service(self, request, *args, **kwargs):
        branch = self.get_object()
        id = request.data.get('id')
        if type(id) != int:
            return Response(data="You must enter the id as an int type", status=status.HTTP_400_BAD_REQUEST)
        data = branch.postal_service.filter(id=id)
        if not data:
            return Response(data="No such postal service", status=status.HTTP_404_NOT_FOUND)
        branch.postal_service.remove(data.first())
        shablon_service = ShablonServices.objects.get(id=id)
        shablon_service.delete()
        return Response(data="successful deleted", status=status.HTTP_204_NO_CONTENT)
    #
    #
    #

    @action(detail=True, methods=['post'])
    def kurier_services(self, request, *args, **kwargs):
        branch = self.get_object()
        serializer = ShablonServicesSerializer(data=request.data)
        if serializer.is_valid():
            postal_service = serializer.save()
            branch.kurier_services.add(postal_service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @kurier_services.mapping.put
    def update_kurier_service(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        branch = self.get_object()
        kurier_service = branch.kurier_services.filter(id=id).first()
        if kurier_service is None:
            return Response(data="kurier usluga not found", status=status.HTTP_404_NOT_FOUND)
        serializer = ShablonServicesSerializer(kurier_service, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @kurier_services.mapping.delete
    def delete_kurier_service(self, request, *args, **kwargs):
        branch = self.get_object()
        id = request.data.get('id')
        if type(id) != int:
            return Response(data="You must enter the id as an int type", status=status.HTTP_400_BAD_REQUEST)
        data = branch.kurier_services.filter(id=id)
        if not data:
            return Response(data="No such menu element", status=status.HTTP_404_NOT_FOUND)
        branch.kurier_services.remove(data.first())
        shablon_service = ShablonServices.objects.get(id=id)
        shablon_service.delete()
        return Response(data="successful deleted", status=status.HTTP_204_NO_CONTENT)
    #
    #
    #

    @action(detail=True, methods=['post'])
    def additional_services(self, request, *args, **kwargs):
        branch = self.get_object()
        serializer = ShablonServicesSerializer(data=request.data)
        if serializer.is_valid():
            postal_service = serializer.save()
            branch.additional_services.add(postal_service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @additional_services.mapping.put
    def update_additional_service(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        branch = self.get_object()
        additional_service = branch.additional_services.filter(id=id).first()
        if additional_service is None:
            return Response(data="additional service not found", status=status.HTTP_404_NOT_FOUND)
        serializer = ShablonServicesSerializer(additional_service, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @additional_services.mapping.delete
    def delete_additional_service(self, request, *args, **kwargs):
        branch = self.get_object()
        id = request.data.get('id')
        if type(id) != int:
            return Response(data="You must enter the id as an int type", status=status.HTTP_400_BAD_REQUEST)
        data = branch.additional_services.filter(id=id)
        if not data:
            return Response(data="No such additional services", status=status.HTTP_404_NOT_FOUND)
        branch.additional_services.remove(data.first())
        shablon_service = ShablonServices.objects.get(id=id)
        shablon_service.delete()
        return Response(data="successful deleted", status=status.HTTP_204_NO_CONTENT)

    #
    #
    #
    @action(detail=True, methods=['post'])
    def contractual_services(self, request, *args, **kwargs):
        branch = self.get_object()
        serializer = ShablonServicesSerializer(data=request.data)
        if serializer.is_valid():
            contractual_services = serializer.save()
            branch.contractual_services.add(contractual_services)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @contractual_services.mapping.put
    def update_contractual_service(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        branch = self.get_object()
        contractual_services = branch.contractual_services.filter(id=id).first()
        if contractual_services is None:
            return Response(data="contractual usluga not found", status=status.HTTP_404_NOT_FOUND)
        serializer = ShablonServicesSerializer(contractual_services, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @contractual_services.mapping.delete
    def delete_contractual_service(self, request, *args, **kwargs):
        branch = self.get_object()
        id = request.data.get('id')
        if type(id) != int:
            return Response(data="You must enter the id as an int type", status=status.HTTP_400_BAD_REQUEST)
        data = branch.contractual_services.filter(id=id)
        if not data:
            return Response(data="No such contractual services", status=status.HTTP_404_NOT_FOUND)
        branch.contractual_services.remove(data.first())
        shablon_service = ShablonServices.objects.get(id=id)
        shablon_service.delete()
        return Response(data="successful deleted", status=status.HTTP_204_NO_CONTENT)
    #
    #
    #

    @action(detail=True, methods=['post'])
    def modern_ict_services(self, request, *args, **kwargs):
        branch = self.get_object()
        serializer = ShablonServicesSerializer(data=request.data)
        if serializer.is_valid():
            modern_ict_service = serializer.save()
            branch.modern_ict_services.add(modern_ict_service)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @modern_ict_services.mapping.put
    def update_modern_ict_services(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        branch = self.get_object()
        kurier_service = branch.modern_ict_services.filter(id=id).first()
        if kurier_service is None:
            return Response(data="modern_ict_services not found", status=status.HTTP_404_NOT_FOUND)
        serializer = ShablonServicesSerializer(kurier_service, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @modern_ict_services.mapping.delete
    def delete_modern_ict_services(self, request, *args, **kwargs):
        branch = self.get_object()
        id = request.data.get('id')
        if type(id) != int:
            return Response(data="You must enter the id as an int type", status=status.HTTP_400_BAD_REQUEST)
        data = branch.modern_ict_services.filter(id=id)
        if not data:
            return Response(data="No such modern_ict_services", status=status.HTTP_404_NOT_FOUND)
        branch.modern_ict_services.remove(data.first())
        shablon_service = ShablonServices.objects.get(id=id)
        shablon_service.delete()
        return Response(data="successful deleted", status=status.HTTP_204_NO_CONTENT)


class VacanciesImagesAPIViewSet(ModelViewSet):
    queryset = VacanciesImages.objects.all()
    serializer_class = VacanciesImagesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class InternalDocumentsAPIViewSet(ModelViewSet):
    queryset = InternalDocuments.objects.all()
    serializer_class = InternalDocumentsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class ThemaQuestionsAPIViewSet(ModelViewSet):
    queryset = ThemaQuestions.objects.all()
    serializer_class = ThemaQuestionsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class BusinessPlansCompletedAPIViewSet(ModelViewSet):
    queryset = BusinessPlansCompleted.objects.all()
    serializer_class = BusinessPlansCompletedSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class AnnualReportsAPIViewSet(ModelViewSet):
    queryset = AnnualReports.objects.all()
    serializer_class = AnnualReportsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class DividendsAPIViewSet(ModelViewSet):
    queryset = Dividends.objects.all()
    serializer_class = DividendsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class QuarterReportsAPIViewSet(ModelViewSet):
    queryset = QuarterReports.objects.all()
    serializer_class = QuarterReportsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class UserInstructionsAPIViewSet(ModelViewSet):
    queryset = UserInstructions.objects.all()
    serializer_class = UserInstructionsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class ExecutiveApparatusAPIViewSet(ModelViewSet):
    queryset = ExecutiveApparatus.objects.all()
    serializer_class = ExecutiveApparatusSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class ShablonUzPostTelNumberAPIViewSet(ModelViewSet):
    queryset = ShablonUzPostTelNumber.objects.all()
    serializer_class = ShablonUzPostTelNumberSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]


class ShablonContactSpecialTitleAPIViewSet(ModelViewSet):
    queryset = ShablonContactSpecialTitle.objects.all()
    serializer_class = ShablonContactSpecialTitleSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]


class ContactAPIViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()
    """
    contact uchun shablonlar many to many actions
    """
    @action(detail=True, methods=['post'])
    def tel_number(self, request, *args, **kwargs):
        contact = self.get_object()
        serializer = ShablonUzPostTelNumberSerializer(data=request.data)
        if serializer.is_valid():
            tel_number = serializer.save()
            contact.tel_number.add(tel_number)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @tel_number.mapping.put
    def update_tel_number(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        contact = self.get_object()
        tel_number = contact.tel_number.filter(id=id).first()
        if tel_number is None:
            return Response(data="tel number not found", status=status.HTTP_404_NOT_FOUND)
        serializer = ShablonUzPostTelNumberSerializer(tel_number, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @tel_number.mapping.delete
    def delete_tel_number(self, request, *args, **kwargs):
        contact = self.get_object()
        id = request.data.get('id')
        if type(id) != int:
            return Response(data="You must enter the id as an int type", status=status.HTTP_400_BAD_REQUEST)
        data = contact.tel_number.filter(id=id)
        if not data:
            return Response(data="No such tel number", status=status.HTTP_404_NOT_FOUND)
        contact.tel_number.remove(data.first())
        shablon_tel_number = ShablonUzPostTelNumber.objects.get(id=id)
        shablon_tel_number.delete()
        return Response(data="successful deleted", status=status.HTTP_204_NO_CONTENT)
    #
    #
    #

    @action(detail=True, methods=['post'])
    def title_2(self, request, *args, **kwargs):
        contact = self.get_object()
        serializer = ShablonContactSpecialTitleSerializer(data=request.data)
        if serializer.is_valid():
            title_2 = serializer.save()
            contact.title_2.add(title_2)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @title_2.mapping.put
    def update_title_2(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        contact = self.get_object()
        title_2 = contact.title_2.filter(id=id).first()
        if title_2 is None:
            return Response(data="title_2 not found", status=status.HTTP_404_NOT_FOUND)
        serializer = ShablonContactSpecialTitleSerializer(title_2, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @title_2.mapping.delete
    def delete_title_2(self, request, *args, **kwargs):
        contact = self.get_object()
        id = request.data.get('id')
        if type(id) != int:
            return Response(data="You must enter the id as an int type", status=status.HTTP_400_BAD_REQUEST)
        data = contact.title_2.filter(id=id)
        if not data:
            return Response(data="No such title_2", status=status.HTTP_404_NOT_FOUND)
        contact.title_2.remove(data.first())
        shablon_title_2 = ShablonContactSpecialTitle.objects.get(id=id)
        shablon_title_2.delete()
        return Response(data="successful deleted", status=status.HTTP_204_NO_CONTENT)

    #
    #
    #

    @action(detail=True, methods=['post'])
    def description_2(self, request, *args, **kwargs):
        contact = self.get_object()
        serializer = ShablonContactSpecialTitleSerializer(data=request.data)
        if serializer.is_valid():
            description_2 = serializer.save()
            contact.description_2.add(description_2)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @description_2.mapping.put
    def update_description_2(self, request, *args, **kwargs):
        id = request.data.get('id')
        if type(id) != int or id is None:
            return Response(data="Try to enter the correct id", status=status.HTTP_400_BAD_REQUEST)
        contact = self.get_object()
        description_2 = contact.description_2.filter(id=id).first()
        if description_2 is None:
            return Response(data="description_2 not found", status=status.HTTP_404_NOT_FOUND)
        serializer = ShablonContactSpecialTitleSerializer(description_2, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    @description_2.mapping.delete
    def delete_description_2(self, request, *args, **kwargs):
        contact = self.get_object()
        id = request.data.get('id')
        if type(id) != int:
            return Response(data="You must enter the id as an int type", status=status.HTTP_400_BAD_REQUEST)
        data = contact.description_2.filter(id=id)
        if not data:
            return Response(data="No such description_2", status=status.HTTP_404_NOT_FOUND)
        contact.description_2.remove(data.first())
        shablon_description_2 = ShablonContactSpecialTitle.objects.get(id=id)
        shablon_description_2.delete()
        return Response(data="successful deleted", status=status.HTTP_204_NO_CONTENT)


class AdvertisementsAPIViewSet(ModelViewSet):
    queryset = Advertisements.objects.all()
    serializer_class = AdvertisementsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class OrganicManagementsAPIViewSet(ModelViewSet):
    queryset = OrganicManagements.objects.all()
    serializer_class = OrganicManagementsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class PartnersAPIViewSet(ModelViewSet):
    queryset = Partners.objects.all()
    serializer_class = PartnersSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class RegionalBranchesAPIViewSet(ModelViewSet):
    queryset = RegionalBranches.objects.all()
    serializer_class = RegionalBranchesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class AdvertisingAPIViewSet(ModelViewSet):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class InformationAboutIssuerAPIViewSet(ModelViewSet):
    queryset = InformationAboutIssuer.objects.all()
    serializer_class = InformationAboutIssuerSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class SlidesAPIViewSet(ModelViewSet):
    queryset = Slides.objects.all()
    serializer_class = SlidesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class SocialMediaAPIViewSet(ModelViewSet):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class EssentialFactsAPIViewSet(ModelViewSet):
    queryset = EssentialFacts.objects.all()
    serializer_class = EssentialFactsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class RatesAPIViewSet(ModelViewSet):
    queryset = Rates.objects.all()
    serializer_class = RatesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class ServicesAPIViewSet(ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class CharterSocietyAPIViewSet(ModelViewSet):
    queryset = CharterSociety.objects.all()
    serializer_class = CharterSocietySerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class SecurityPapersAPIViewSet(ModelViewSet):
    queryset = SecurityPapers.objects.all()
    serializer_class = SecurityPapersSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class FAQAPIViewSet(ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.save_image:
            if os.path.isfile(instance.save_image.path):
                os.remove(instance.save_image.path)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        # Oldingi rasm faylini o'chirish
        if 'save_image' in request.data and not request.data['save_image']:
            if instance.save_image:
                if os.path.isfile(instance.save_image.path):
                    os.remove(instance.save_image.path)
                instance.save_image = None

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class SiteSettingsAPIViewSet(ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [AllowAny, IsCustomUsersGet]
    throttle_classes = [CustomUserThrottle, ]

