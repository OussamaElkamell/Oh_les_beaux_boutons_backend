"""
URL configuration for nird_api project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

# Import your custom token view from the users app
from users.views import MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),

    # API endpoints
    path('api/cards/', include('cards.urls')),
    path('api/results/', include('results.urls')),
    path('api/users/', include('users.urls')),

    # JWT Authentication
    path('api/auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
