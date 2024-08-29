from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Punto de entrada global para todas las vistas bajo 'api/'
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def protected_view(request):
    pass

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', protected_view),  # Punto de entrada global
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('web_elect.urls')),
]
