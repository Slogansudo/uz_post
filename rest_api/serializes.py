from models.models import CustomUser, UsersRequests
from rest_framework import serializers
from db_models.models import (Banners, MenuElements, Menu, StatisticItems, Statistics, TegRegions, TegWorkingDays,
                              TegExperience, TegVacancies, TegBranches2, Vacancies, Purchases, Marks, SaveMediaFiles,
                              Events, UzPostNews, PostalServices, Pages, BranchServices, ShablonServices, Branches,
                              VacanciesImages, InternalDocuments, ThemaQuestions, BusinessPlansCompleted, AnnualReports,
                              Dividends, QuarterReports, UserInstructions, ExecutiveApparatus, ShablonUzPostTelNumber,
                              ShablonContactSpecialTitle, Contact, Advertisements, OrganicManagements, Partners,
                              RegionalBranches, Advertising, InformationAboutIssuer, Slides, SocialMedia, EssentialFacts,
                              Rates, Services, CharterSociety, SecurityPapers, FAQ, SiteSettings)
from django.db import transaction
from django.contrib.auth.models import Group, Permission


class PermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionsSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = '__all__'
        read_only_fields = ["id"]


class CustomUserSerializer(serializers.ModelSerializer):
    # Userlar ro'yhatini ko'rish yangi user qo'shish o'chirish imkonini beruvchi serializer
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"
        read_only_fields = ["id"]


class UsersRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersRequests
        fields = "__all__"
        read_only_fields = ["id"]


class BannersSerializer(serializers.ModelSerializer):
    # banners jadvali uchun serializer
    class Meta:
        model = Banners
        fields = "__all__"
        read_only_fields = ["id"]


class MenuElementsSerializer(serializers.ModelSerializer):
    # menu elements jadvali uchun serializer

    class Meta:
        model = MenuElements
        fields = "__all__"


class MenuSerializer(serializers.ModelSerializer):
    # menu jadvali uchun  serializer class
    menu_elements = MenuElementsSerializer(many=True, read_only=True)
    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ["id"]


class StatisticItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatisticItems
        fields = "__all__"
        read_only_fields = ["id"]


class StatisticsSerializer(serializers.ModelSerializer):
    statistic_items = StatisticItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Statistics
        fields = "__all__"
        read_only_fields = ["id"]


class TegRegionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TegRegions
        fields = "__all__"
        read_only_fields = ["id"]


class TegWorkingDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = TegWorkingDays
        fields = "__all__"
        read_only_fields = ["id"]


class TegExperiencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TegExperience
        fields = "__all__"
        read_only_fields = ["id"]


class TegVacanciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TegVacancies
        fields = "__all__"
        read_only_fields = ["id"]


class TegBranches2Serializer(serializers.ModelSerializer):
    class Meta:
        model = TegBranches2
        fields = "__all__"
        read_only_fields = ["id"]


class VacanciesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vacancies
        fields = "__all__"
        read_only_fields = ["id"]


class PurchasesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchases
        fields = "__all__"
        read_only_fields = ["id"]


class MarksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marks
        fields = "__all__"
        read_only_fields = ["id"]


class SaveMediaFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveMediaFiles
        fields = "__all__"
        read_only_fields = ["id"]


class EventsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        fields = "__all__"
        read_only_fields = ["id"]


class UzPostNewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = UzPostNews
        fields = "__all__"
        read_only_fields = ["id"]


class PostalServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostalServices
        fields = "__all__"
        read_only_fields = ["id"]


class PagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pages
        fields = "__all__"
        read_only_fields = ["id"]


class BranchServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchServices
        fields = "__all__"
        read_only_fields = ["id"]


class ShablonServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShablonServices
        fields = "__all__"
        read_only_fields = ["id"]


class BranchesSerializer(serializers.ModelSerializer):
    postal_service = ShablonServicesSerializer(many=True, read_only=True)
    kurier_services = ShablonServicesSerializer(many=True, read_only=True)
    additional_services = ShablonServicesSerializer(many=True, read_only=True)
    contractual_services = ShablonServicesSerializer(many=True, read_only=True)
    modern_ict_services = ShablonServicesSerializer(many=True, read_only=True)

    class Meta:
        model = Branches
        fields = "__all__"
        read_only_fields = ["id"]


class VacanciesImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacanciesImages
        fields = "__all__"
        read_only_fields = ["id"]


class InternalDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InternalDocuments
        fields = "__all__"
        read_only_fields = ["id"]


class ThemaQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThemaQuestions
        fields = "__all__"
        read_only_fields = ["id"]


class BusinessPlansCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessPlansCompleted
        fields = "__all__"
        read_only_fields = ["id"]


class AnnualReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnualReports
        fields = "__all__"
        read_only_fields = ["id"]


class DividendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dividends
        fields = "__all__"
        read_only_fields = ["id"]


class QuarterReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuarterReports
        fields = "__all__"
        read_only_fields = ["id"]


class UserInstructionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInstructions
        fields = "__all__"
        read_only_fields = ["id"]


class ExecutiveApparatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExecutiveApparatus
        fields = "__all__"
        read_only_fields = ["id"]


class ShablonUzPostTelNumberSerializer(serializers.ModelSerializer):
        class Meta:
            model = ShablonUzPostTelNumber
            fields = "__all__"
            read_only_fields = ["id"]


class ShablonContactSpecialTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShablonContactSpecialTitle
        fields = "__all__"
        read_only_fields = ["id"]


class ContactSerializer(serializers.ModelSerializer):
    tel_number = ShablonUzPostTelNumberSerializer(many=True, read_only=True)
    title_2 = ShablonContactSpecialTitleSerializer(many=True, read_only=True)
    description_2 = ShablonContactSpecialTitleSerializer(many=True, read_only=True)

    class Meta:
        model = Contact
        fields = "__all__"
        read_only_fields = ["id"]


class AdvertisementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisements
        fields = "__all__"
        read_only_fields = ["id"]


class OrganicManagementsSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrganicManagements
        fields = "__all__"
        read_only_fields = ["id"]


class PartnersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Partners
        fields = "__all__"
        read_only_fields = ["id"]


class RegionalBranchesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionalBranches
        fields = "__all__"
        read_only_fields = ["id"]


class AdvertisingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertising
        fields = "__all__"
        read_only_fields = ["id"]


class InformationAboutIssuerSerializer(serializers.ModelSerializer):
    class Meta:
        model = InformationAboutIssuer
        fields = "__all__"
        read_only_fields = ["id"]


class SlidesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slides
        fields = "__all__"
        read_only_fields = ["id"]


class SocialMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMedia
        fields = "__all__"
        read_only_fields = ["id"]


class EssentialFactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EssentialFacts
        fields = "__all__"
        read_only_fields = ["id"]


class RatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rates
        fields = "__all__"
        read_only_fields = ["id"]


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = "__all__"
        read_only_fields = ["id"]


class CharterSocietySerializer(serializers.ModelSerializer):
    class Meta:
        model = CharterSociety
        fields = "__all__"
        read_only_fields = ["id"]


class SecurityPapersSerializer(serializers.ModelSerializer):
    class Meta:
        model = SecurityPapers
        fields = "__all__"
        read_only_fields = ["id"]


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = "__all__"
        read_only_fields = ["id"]


class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"
        read_only_fields = ["id"]

