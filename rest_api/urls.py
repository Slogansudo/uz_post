from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import (UsersAPIView, UsersDetailAPIView, UserRequestsView, UsersRequestsDetailView, BannerAPIViewSet, MenuElementsAPIViewSet, MenuAPIViewSet,
                  StatisticItemsAPIViewSet, StatisticsAPIViewSet, VacanciesAPIViewSet, TegRegionsAPIViewSet,
                    TegWorkingDaysAPIViewSet, TegExperiencesAPIViewSet, TegVacanciesAPIViewSet, TegBranches2APIViewSet,
                    PurchasesAPIViewSet, MarksAPIViewSet, SaveMediaFilesAPIViewSet, EventsAPIViewSet, UzPostNewsAPIViewSet,
                    PostalServicesAPIViewSet, PagesAPIViewSet, BranchServicesAPIViewSet, ShablonServicesAPIViewSet,
                    BranchesAPIViewSet, VacanciesImagesAPIViewSet, InternalDocumentsAPIViewSet, ThemaQuestionsAPIViewSet,
                    BusinessPlansCompletedAPIViewSet, AnnualReportsAPIViewSet, DividendsAPIViewSet, QuarterReportsAPIViewSet,
                    UserInstructionsAPIViewSet, ExecutiveApparatusAPIViewSet, ShablonUzPostTelNumberAPIViewSet,
                    ShablonContactSpecialTitleAPIViewSet, ContactAPIViewSet, AdvertisementsAPIViewSet, OrganicManagementsAPIViewSet,
                    PartnersAPIViewSet, RegionalBranchesAPIViewSet, AdvertisingAPIViewSet, InformationAboutIssuerAPIViewSet,
                    SlidesAPIViewSet, SocialMediaAPIViewSet, EssentialFactsAPIViewSet, RatesAPIViewSet, ServicesAPIViewSet, CharterSocietyAPIViewSet,
                    SecurityPapersAPIViewSet, FAQAPIViewSet, SiteSettingsAPIViewSet, CategoryPagesViewSet, ControlCategoryPageViewSet)
schema_view = get_schema_view(
    openapi.Info(
        title="UzPOST API",
        default_version='v1',
        description="Demo UzPOST API",
        terms_of_service='demo.com',
        contact=openapi.Contact(email='<EMAIL>'),
        license=openapi.License(name='demo service')
    ),
    public=True,
    permission_classes=(permissions.IsAuthenticated, )
)

router = DefaultRouter()
router.register("banners", viewset=BannerAPIViewSet)
router.register("menu-elements", viewset=MenuElementsAPIViewSet)
router.register("menu", viewset=MenuAPIViewSet)
router.register("statistic-items", viewset=StatisticItemsAPIViewSet)
router.register("statistics", viewset=StatisticsAPIViewSet)
router.register("teg-working-days", viewset=TegWorkingDaysAPIViewSet)
router.register("teg-experiences", viewset=TegExperiencesAPIViewSet)
router.register("teg-vacancies", viewset=TegVacanciesAPIViewSet)
router.register("teg-branches_2", viewset=TegBranches2APIViewSet)
router.register("vacancies", viewset=VacanciesAPIViewSet)
router.register("purchases", viewset=PurchasesAPIViewSet)
router.register("marks", viewset=MarksAPIViewSet)
router.register("save-media-files", viewset=SaveMediaFilesAPIViewSet)
router.register("events", viewset=EventsAPIViewSet)
router.register("uz-post-news", viewset=UzPostNewsAPIViewSet)
router.register("postal-services", viewset=PostalServicesAPIViewSet)
router.register("pages", viewset=PagesAPIViewSet)
router.register("category-pages", viewset=CategoryPagesViewSet)
router.register("control-category-pages", viewset=ControlCategoryPageViewSet)
router.register("branch-services", viewset=BranchServicesAPIViewSet)
router.register("shablon-services", viewset=ShablonServicesAPIViewSet)
router.register("branches", viewset=BranchesAPIViewSet)
router.register("vacancies-images", viewset=VacanciesImagesAPIViewSet)
router.register("internal-documents", viewset=InternalDocumentsAPIViewSet)
router.register("thema-questions", viewset=ThemaQuestionsAPIViewSet)
router.register("business-plans-completed", viewset=BusinessPlansCompletedAPIViewSet)
router.register("annual-reports", viewset=AnnualReportsAPIViewSet)
router.register("dividends", viewset=DividendsAPIViewSet)
router.register("quarter-reports", viewset=QuarterReportsAPIViewSet)
router.register("user-intructions", viewset=UserInstructionsAPIViewSet)
router.register("executive-apparatus", viewset=ExecutiveApparatusAPIViewSet)
router.register("shablon-uz-post-tel_number", viewset=ShablonUzPostTelNumberAPIViewSet)
router.register("shablon-contact-special-title", viewset=ShablonContactSpecialTitleAPIViewSet)
router.register("contact", viewset=ContactAPIViewSet)
router.register("advertisements", viewset=AdvertisementsAPIViewSet)
router.register("organic-managements", viewset=OrganicManagementsAPIViewSet)
router.register("partners", viewset=PartnersAPIViewSet)
router.register("regional-branches", viewset=RegionalBranchesAPIViewSet)
router.register("advertising", viewset=AdvertisingAPIViewSet)
router.register("information-about-issuer", viewset=InformationAboutIssuerAPIViewSet)
router.register("slides", viewset=SlidesAPIViewSet)
router.register("social-media", viewset=SocialMediaAPIViewSet)
router.register("essential-facts", viewset=EssentialFactsAPIViewSet)
router.register("rates", viewset=RatesAPIViewSet)
router.register("services", viewset=ServicesAPIViewSet)
router.register("charter-society", viewset=CharterSocietyAPIViewSet)
router.register("security-papers", viewset=SecurityPapersAPIViewSet)
router.register("faq", viewset=FAQAPIViewSet)
router.register("site-settings", viewset=SiteSettingsAPIViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('users/', UsersAPIView.as_view(), name='users'),
    path('users/<int:id>/', UsersDetailAPIView.as_view(), name='user-detail'),
    path('users-requests/', UserRequestsView.as_view(), name='user-requests'),
    path('users-requests/<int:id>/', UsersRequestsDetailView.as_view(), name='user-requests-detail'),
    path('docs-swagger/', schema_view.with_ui("swagger", cache_timeout=0), name='swagger'),
    path('docs-redoc/', schema_view.with_ui("redoc", cache_timeout=0), name='redoc'),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

