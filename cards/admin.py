from django.contrib import admin
from .models import TechnologyCard, Category, Pillar


@admin.register(Pillar)
class PillarAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'description']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(TechnologyCard)
class TechnologyCardAdmin(admin.ModelAdmin):
    list_display = ['name', 'card_type', 'category', 'pillar', 'cost', 'is_active']
    list_filter = ['card_type', 'pillar', 'category', 'is_active']
    search_fields = ['name', 'card_id', 'description']
    ordering = ['category', 'name']
    
    fieldsets = (
        ('Informations de base', {
            'fields': ('card_id', 'name', 'card_type', 'category', 'pillar', 'description', 'icon')
        }),
        ('Statistiques', {
            'fields': ('cost', 'co2', 'data_location')
        }),
        ('Alternative & Économies', {
            'fields': ('alternative', 'savings_euros', 'savings_co2_kg'),
            'classes': ('collapse',)
        }),
        ('Statut', {
            'fields': ('is_active',)
        }),
    )
