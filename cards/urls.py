from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TechnologyCardViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r'', TechnologyCardViewSet, basename='card')
router.register(r'categories', CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls)),
]
