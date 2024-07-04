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


class CustomUserSerializer(serializers.ModelSerializer):
    # Userlar ro'yhatini ko'rish yangi user qo'shish o'chirish imkonini beruvchi serializer
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
    banner = BannersSerializer()

    class Meta:
        model = MenuElements
        fields = "__all__"
        read_only_fields = ["id"]

class MenuSerializer(serializers.ModelSerializer):
    # menu jadvali uchun  serializer class
    menu_elements = MenuElementsSerializer(many=True)

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ["id"]


class StatisticItemsSerializer(serializers.ModelSerializer):
    # statistics jadvali uchun  serializer
    class Meta:
        model = StatisticItems
        fields = "__all__"
        read_only_fields = ["id"]


class StatisticsSerializer(serializers.ModelSerializer):

    statistic_items = StatisticItemsSerializer(many=True)

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
    teg_vacancies = TegVacanciesSerializer(many=True)
    teg_experiences = TegExperiencesSerializer(many=True)
    teg_regions = TegRegionsSerializer(many=True)

    class Meta:
        model = Vacancies
        fields = "__all__"
        read_only_fields = ["id"]

    def create(self, validated_data):
        teg_vacancies_data = validated_data.pop('teg_vacancies')
        teg_experiences_data = validated_data.pop('teg_experiences')
        teg_regions_data = validated_data.pop('teg_regions')

        vacancies = Vacancies.objects.create(**validated_data)

        for teg_vacancy_data in teg_vacancies_data:
            teg_vacancy, created = TegVacancies.objects.get_or_create(**teg_vacancy_data)
            vacancies.teg_vacancies.add(teg_vacancy)

        for teg_experience_data in teg_experiences_data:
            teg_experience, created = TegExperience.objects.get_or_create(**teg_experience_data)
            vacancies.teg_experiences.add(teg_experience)

        for teg_region_data in teg_regions_data:
            teg_region, created = TegRegions.objects.get_or_create(**teg_region_data)
            vacancies.teg_regions.add(teg_region)

        return vacancies

    def update(self, instance, validated_data):
        teg_vacancies_data = validated_data.pop('teg_vacancies')
        teg_experiences_data = validated_data.pop('teg_experiences')
        teg_regions_data = validated_data.pop('teg_regions')

        instance.title_ru = validated_data.get('title_ru', instance.title_ru)
        instance.title_uz = validated_data.get('title_uz', instance.title_uz)
        instance.description_ru = validated_data.get('description_ru', instance.description_ru)
        instance.description_uz = validated_data.get('description_uz', instance.description_uz)
        # Boshqa maydonlarni yangilang
        instance.save()

        instance.teg_vacancies.clear()
        for teg_vacancy_data in teg_vacancies_data:
            teg_vacancy, created = TegVacancies.objects.get_or_create(**teg_vacancy_data)
            instance.teg_vacancies.add(teg_vacancy)

        instance.teg_experiences.clear()
        for teg_experience_data in teg_experiences_data:
            teg_experience, created = TegExperience.objects.get_or_create(**teg_experience_data)
            instance.teg_experiences.add(teg_experience)

        instance.teg_regions.clear()
        for teg_region_data in teg_regions_data:
            teg_region, created = TegRegions.objects.get_or_create(**teg_region_data)
            instance.teg_regions.add(teg_region)

        return instance


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
    video_preview = SaveMediaFilesSerializer(many=True)
    video = SaveMediaFilesSerializer(many=True)
    teg_branches = TegBranches2Serializer(many=True)

    class Meta:
        model = Events
        fields = "__all__"
        read_only_fields = ["id"]


class UzPostNewsSerializer(serializers.ModelSerializer):
    image_ru = SaveMediaFilesSerializer(many=True)
    image_uz = SaveMediaFilesSerializer(many=True)
    video_preview_ru = SaveMediaFilesSerializer(many=True)
    video_preview_uz = SaveMediaFilesSerializer(many=True)
    video_ru = SaveMediaFilesSerializer(many=True)
    video_uz = SaveMediaFilesSerializer(many=True)

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
        model = Branches
        fields = "__all__"
        read_only_fields = ["id"]


class ShablonServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShablonServices
        fields = "__all__"
        read_only_fields = ["id"]


class BranchesSerializer(serializers.ModelSerializer):
    header_image = SaveMediaFilesSerializer(many=True)
    branch_sidebar_image = SaveMediaFilesSerializer(many=True)
    postal_service = ShablonServicesSerializer(many=True)
    kurier_services = ShablonServicesSerializer(many=True)
    additional_services = ShablonServicesSerializer(many=True)
    contractual_services = ShablonServicesSerializer(many=True)
    modern_ict_services = ShablonServicesSerializer(many=True)
    working_days = TegWorkingDaysSerializer(many=True)

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
    tel_number = ShablonUzPostTelNumberSerializer(many=True)
    title_2 = ShablonContactSpecialTitleSerializer(many=True)
    description_2 = ShablonContactSpecialTitleSerializer(many=True)

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
    working_days = TegWorkingDaysSerializer(many=True)

    class Meta:
        model = OrganicManagements
        fields = "__all__"
        read_only_fields = ["id"]


class PartnersSerializer(serializers.ModelSerializer):
    image_ru = SaveMediaFilesSerializer(many=True)
    image_uz = SaveMediaFilesSerializer(many=True)

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

