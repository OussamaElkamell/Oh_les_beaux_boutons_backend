from rest_framework import serializers
from .models import TechnologyCard, Category, Pillar


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class TechnologyCardSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    stats = serializers.SerializerMethodField()
    savings = serializers.SerializerMethodField()
    alternative_id = serializers.CharField(source='alternative.card_id', read_only=True, allow_null=True)
    
    class Meta:
        model = TechnologyCard
        fields = [
            'id', 'card_id', 'name', 'card_type', 'category_name', 
            'pillar', 'description', 'icon', 'stats', 'savings', 'alternative_id'
        ]
    
    def get_stats(self, obj):
        return {
            'cost': obj.cost,
            'co2': obj.co2,
            'dataLocation': obj.data_location,
        }
    
    def get_savings(self, obj):
        if obj.card_type == 'nird' and (obj.savings_euros > 0 or obj.savings_co2_kg > 0):
            return {
                'euros': obj.savings_euros,
                'co2Kg': obj.savings_co2_kg,
            }
        return None


class TechnologyCardListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    category = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = TechnologyCard
        fields = ['id', 'card_id', 'name', 'card_type', 'category', 'icon']
