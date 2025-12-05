from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'school_name', 'school_type', 'is_active', 'created_at']
    list_filter = ['school_type', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'school_name']
    ordering = ['-created_at']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informations École', {'fields': ('school_name', 'school_type')}),
    )
    
    inlines = [UserProfileInline]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'total_games_played', 'best_nird_score', 'total_points_earned']
    search_fields = ['user__username', 'user__email']
