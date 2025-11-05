from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.keys.v1.views import KeyItemViewSet, FolderViewSet


router = DefaultRouter()
router.register(r'items', KeyItemViewSet, basename='keyitem')
router.register(r'folders', FolderViewSet, basename='folder')

urlpatterns = router.urls
