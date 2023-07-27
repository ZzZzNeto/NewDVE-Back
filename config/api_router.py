from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter, SimpleRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from newdve_back.announces.api.viewsets import AnnounceViewSet, TagViewSet, Announce_imageViewSet, RatingViewSet
from newdve_back.users.api.viewsets import UserViewSet, User_fileViewSet, AddresViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet, basename='users')
router.register("user_files", User_fileViewSet, basename='user_files'),
router.register("addresses", AddresViewSet, basename='addresses')

router.register("announces", AnnounceViewSet, basename='announces')
router.register("tags", TagViewSet, basename='tags')
router.register("announce_images", Announce_imageViewSet, basename='announce_images')
router.register("ratings", RatingViewSet, basename='ratings')

app_name = "api"
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
] + router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
