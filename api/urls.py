from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from accounts.views import RegisterView, UserProfileView
from campaigns.views import CampaignViewSet, CategoryViewSet
from donations.views import DonationViewSet

from .views import ChatBotView

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'donations', DonationViewSet, basename='donation')

urlpatterns = [
    # ChatBot
    path('chat/', ChatBotView.as_view(), name='api_chat'),

    # Auth JWT
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/profile/', UserProfileView.as_view(), name='auth_profile'),

    # App Routers
    path('', include(router.urls)),
    
    # Payments
    path('payments/', include('payments.urls')),
    
    # Swagger documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
