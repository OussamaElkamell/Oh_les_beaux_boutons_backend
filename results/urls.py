from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameResultViewSet

router = DefaultRouter()
router.register(r'', GameResultViewSet, basename='result')

urlpatterns = [
    path('', include(router.urls)),
]
