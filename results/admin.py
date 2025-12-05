from django.contrib import admin
from .models import GameResult, GameChoice, WrongAnswer


class GameChoiceInline(admin.TabularInline):
    model = GameChoice
    extra = 0
    readonly_fields = ['card_id', 'card_name', 'card_type', 'accepted', 'points_earned', 'timestamp']


class WrongAnswerInline(admin.TabularInline):
    model = WrongAnswer
    extra = 0


@admin.register(GameResult)
class GameResultAdmin(admin.ModelAdmin):
    list_display = ['user', 'nird_score', 'total_points', 'cards_played', 'correct_choices', 'completed_at']
    list_filter = ['completed_at']
    search_fields = ['user__username', 'user__email', 'session_id']
    ordering = ['-completed_at']
    readonly_fields = ['completed_at']
    
    inlines = [GameChoiceInline, WrongAnswerInline]
    
    fieldsets = (
        ('Utilisateur', {
            'fields': ('user', 'session_id')
        }),
        ('Scores', {
            'fields': ('nird_score', 'total_points', 'cards_played', 'correct_choices')
        }),
        ('Scores par pilier', {
            'fields': ('inclusion_score', 'responsabilite_score', 'durabilite_score')
        }),
        ('Économies', {
            'fields': ('total_savings_euros', 'total_savings_co2')
        }),
        ('Dates', {
            'fields': ('started_at', 'completed_at')
        }),
    )
