from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import GameResult
from .serializers import GameResultSerializer, GameResultCreateSerializer, GameResultListSerializer


class GameResultViewSet(viewsets.ModelViewSet):
    """ViewSet for game results."""
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return GameResult.objects.filter(user=self.request.user)
        return GameResult.objects.none()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return GameResultCreateSerializer
        if self.action == 'list':
            return GameResultListSerializer
        return GameResultSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        
        # Return full result data
        response_serializer = GameResultSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
