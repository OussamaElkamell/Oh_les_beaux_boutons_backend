from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q
import random

from .models import TechnologyCard, Category
from .serializers import TechnologyCardSerializer, TechnologyCardListSerializer, CategorySerializer


class TechnologyCardViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for technology cards."""
    queryset = TechnologyCard.objects.filter(is_active=True)
    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TechnologyCardListSerializer
        return TechnologyCardSerializer
    
    @action(detail=False, methods=['get'])
    def random(self, request):
        """Get a random selection of cards for the game."""
        count = int(request.query_params.get('count', 15))
        
        # Get balanced selection
        big_tech = list(self.queryset.filter(card_type='big-tech'))
        nird = list(self.queryset.filter(card_type='nird'))
        
        random.shuffle(big_tech)
        random.shuffle(nird)
        
        half = count // 2
        selected = big_tech[:half] + nird[:count - half]
        random.shuffle(selected)
        
        serializer = TechnologyCardSerializer(selected, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get cards filtered by category."""
        category_name = request.query_params.get('category')
        if not category_name:
            return Response(
                {"error": "Category parameter required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cards = self.queryset.filter(category__name__icontains=category_name)
        serializer = TechnologyCardSerializer(cards, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_pillar(self, request):
        """Get cards filtered by NIRD pillar."""
        pillar = request.query_params.get('pillar')
        if not pillar:
            return Response(
                {"error": "Pillar parameter required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        cards = self.queryset.filter(pillar=pillar)
        serializer = TechnologyCardSerializer(cards, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
