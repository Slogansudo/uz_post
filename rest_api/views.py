from rest_framework.serializers import ModelSerializer

from .serializes import (CustomUserSerializer, UsersRequestsSerializer, BannersSerializer, MenuElementsSerializer,
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
                         SiteSettingsSerializer)

from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny, BasePermission
from rest_framework.authentication import TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import status, filters
from models.models import CustomUser, UsersRequests
from django.db.transaction import atomic
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from db_models.models import (Banners, MenuElements, Menu, StatisticItems, Statistics, TegRegions, TegWorkingDays,
                              TegExperience, TegVacancies, TegBranches2, Vacancies, Purchases, Marks, SaveMediaFiles,
                              Events, UzPostNews, PostalServices, Pages, BranchServices, ShablonServices, Branches,
                              VacanciesImages, InternalDocuments, ThemaQuestions, BusinessPlansCompleted, AnnualReports,
                              Dividends, QuarterReports, UserInstructions, ExecutiveApparatus, ShablonUzPostTelNumber,
                              ShablonContactSpecialTitle, Contact, Advertisements, OrganicManagements, Partners,
                              RegionalBranches, Advertising, InformationAboutIssuer, Slides, SocialMedia, EssentialFacts,
                              Rates, Services, CharterSociety, SecurityPapers, FAQ, SiteSettings)

import requests
from rest_framework.throttling import UserRateThrottle


class UsersAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        user = request.user
        if user.is_staff:
            users = CustomUser.objects.all()
            serializer = CustomUserSerializer(users, many=True)
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data="not found")

    def post(self, request):
        user = request.user
        if user.is_staff:
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save(password=make_password(serializer.validated_data['password']))
                user.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST, data="not found")


class UsersDetailAPIView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, id):
        user = request.user
        if user.is_staff:
            user_instance = get_object_or_404(CustomUser, id=id)
            serializer = CustomUserSerializer(user_instance)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST, data="not authorized")

    def put(self, request, id):
        user = request.user
        if user.is_staff:
            user_instance = get_object_or_404(CustomUser, id=id)
            serializer = CustomUserSerializer(instance=user_instance, data=request.data)
            if serializer.is_valid():
                user = serializer.save(password=make_password(serializer.validated_data['password']))
                user.save()
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        return Response(status=status.HTTP_400_BAD_REQUEST, data="not found")

    def delete(self, request, id):
        user = request.user
        if user.is_staff:
            user_instance = get_object_or_404(CustomUser, id=id)
            if user_instance.is_active:
                user_instance.delete()
                return Response(status=status.HTTP_204_NO_CONTENT, data="deleted successfully")
            else:
                return Response(status=status.HTTP_404_NOT_FOUND, data="not found")


class UserRequestsView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        data = UsersRequests.objects.all()
        serializer = UsersRequestsSerializer(instance=data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersRequestsDetailView(APIView):
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get(self, request, id):
        data = get_object_or_404(UsersRequests, id=id)
        serializer = UsersRequestsSerializer(instance=data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, id):
        data = get_object_or_404(UsersRequests, id=id)
        if data.is_active:
            data.delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data="successfully deleted")
        return Response(status=status.HTTP_404_NOT_FOUND)


class BannerAPIViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser, IsAuthenticated]

    queryset = Banners.objects.all()
    serializer_class = BannersSerializer


class MenuElementsAPIViewSet(viewsets.ModelViewSet):
    queryset = MenuElements.objects.all()
    serializer_class = MenuElementsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class MenuAPIViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class StatisticItemsAPIViewSet(viewsets.ModelViewSet):
    queryset = StatisticItems.objects.all()
    serializer_class = StatisticItemsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class StatisticsAPIViewSet(viewsets.ModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class TegRegionsAPIViewSet(viewsets.ModelViewSet):
    queryset = TegRegions.objects.all()
    serializer_class = TegRegionsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class TegWorkingDaysAPIViewSet(viewsets.ModelViewSet):
    queryset = TegWorkingDays.objects.all()
    serializer_class = TegWorkingDaysSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class TegExperiencesAPIViewSet(viewsets.ModelViewSet):
    queryset = TegExperience.objects.all()
    serializer_class = TegExperiencesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]


class TegVacanciesAPIViewSet(viewsets.ModelViewSet):
    queryset = TegVacancies.objects.all()
    serializer_class = TegVacanciesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class TegBranches2APIViewSet(viewsets.ModelViewSet):
    queryset = TegBranches2.objects.all()
    serializer_class = TegBranches2Serializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class VacanciesAPIViewSet(ModelViewSet):
    queryset = Vacancies.objects.all()
    serializer_class = VacanciesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class PurchasesAPIViewSet(ModelViewSet):
    queryset = Purchases.objects.all()
    serializer_class = PurchasesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class MarksAPIViewSet(ModelViewSet):
    queryset = Marks.objects.all()
    serializer_class = MarksSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class SaveMediaFilesAPIViewSet(ModelViewSet):
    queryset = SaveMediaFiles.objects.all()
    serializer_class = SaveMediaFilesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class EventsAPIViewSet(ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class UzPostNewsAPIViewSet(ModelViewSet):
    queryset = UzPostNews.objects.all()
    serializer_class = UzPostNewsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class PostalServicesAPIViewSet(ModelViewSet):
    queryset = PostalServices.objects.all()
    serializer_class = PostalServicesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class PagesAPIViewSet(ModelViewSet):
    queryset = Pages.objects.all()
    serializer_class = PagesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class BranchServicesAPIViewSet(ModelViewSet):
    queryset = BranchServices.objects.all()
    serializer_class = BranchServicesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ShablonServicesAPIViewSet(ModelViewSet):
    queryset = ShablonServices.objects.all()
    serializer_class = ShablonServicesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class BranchesAPIViewSet(ModelViewSet):
    queryset = Branches.objects.all()
    serializer_class = BranchesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class VacanciesImagesAPIViewSet(ModelViewSet):
    queryset = VacanciesImages.objects.all()
    serializer_class = VacanciesImagesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class InternalDocumentsAPIViewSet(ModelViewSet):
    queryset = InternalDocuments.objects.all()
    serializer_class = InternalDocumentsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ThemaQuestionsAPIViewSet(ModelViewSet):
    queryset = ThemaQuestions.objects.all()
    serializer_class = ThemaQuestionsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class BusinessPlansCompletedAPIViewSet(ModelViewSet):
    queryset = BusinessPlansCompleted.objects.all()
    serializer_class = BusinessPlansCompletedSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class AnnualReportsAPIViewSet(ModelViewSet):
    queryset = AnnualReports.objects.all()
    serializer_class = AnnualReportsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class DividendsAPIViewSet(ModelViewSet):
    queryset = Dividends.objects.all()
    serializer_class = DividendsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class QuarterReportsAPIViewSet(ModelViewSet):
    queryset = QuarterReports.objects.all()
    serializer_class = QuarterReportsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class UserInstructionsAPIViewSet(ModelViewSet):
    queryset = UserInstructions.objects.all()
    serializer_class = UserInstructionsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ExecutiveApparatusAPIViewSet(ModelViewSet):
    queryset = ExecutiveApparatus.objects.all()
    serializer_class = ExecutiveApparatusSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ShablonUzPostTelNumberAPIViewSet(ModelViewSet):
    queryset = ShablonUzPostTelNumber.objects.all()
    serializer_class = ShablonUzPostTelNumberSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ShablonContactSpecialTitleAPIViewSet(ModelViewSet):
    queryset = ShablonContactSpecialTitle.objects.all()
    serializer_class = ShablonContactSpecialTitleSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ContactAPIViewSet(ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class AdvertisementsAPIViewSet(ModelViewSet):
    queryset = Advertisements.objects.all()
    serializer_class = AdvertisementsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class OrganicManagementsAPIViewSet(ModelViewSet):
    queryset = OrganicManagements.objects.all()
    serializer_class = OrganicManagementsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class PartnersAPIViewSet(ModelViewSet):
    queryset = Partners.objects.all()
    serializer_class = PartnersSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class RegionalBranchesAPIViewSet(ModelViewSet):
    queryset = RegionalBranches.objects.all()
    serializer_class = RegionalBranchesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class AdvertisingAPIViewSet(ModelViewSet):
    queryset = Advertising.objects.all()
    serializer_class = AdvertisingSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class InformationAboutIssuerAPIViewSet(ModelViewSet):
    queryset = InformationAboutIssuer.objects.all()
    serializer_class = InformationAboutIssuerSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class SlidesAPIViewSet(ModelViewSet):
    queryset = Slides.objects.all()
    serializer_class = SlidesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class SocialMediaAPIViewSet(ModelViewSet):
    queryset = SocialMedia.objects.all()
    serializer_class = SocialMediaSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class EssentialFactsAPIViewSet(ModelViewSet):
    queryset = EssentialFacts.objects.all()
    serializer_class = EssentialFactsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class RatesAPIViewSet(ModelViewSet):
    queryset = Rates.objects.all()
    serializer_class = RatesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class ServicesAPIViewSet(ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class CharterSocietyAPIViewSet(ModelViewSet):
    queryset = CharterSociety.objects.all()
    serializer_class = CharterSocietySerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class SecurityPapersAPIViewSet(ModelViewSet):
    queryset = SecurityPapers.objects.all()
    serializer_class = SecurityPapersSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class FAQAPIViewSet(ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]


class SiteSettingsAPIViewSet(ModelViewSet):
    queryset = SiteSettings.objects.all()
    serializer_class = SiteSettingsSerializer
    permission_classes = [IsAdminUser, IsAuthenticated]
    throttle_classes = [UserRateThrottle]





