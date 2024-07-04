from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import ShipmentTrackingAPIView, Tracking

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
    permission_classes=(permissions.AllowAny, )
)

router = DefaultRouter()


urlpatterns = [
    path('docs-swagger/', schema_view.with_ui("swagger", cache_timeout=0), name='swagger'),
    path('docs-redoc/', schema_view.with_ui("redoc", cache_timeout=0), name='redoc'),
    path('tracking/', ShipmentTrackingAPIView.as_view(), name='tracing'),
    path('track/', Tracking.as_view(), name='track')

]
