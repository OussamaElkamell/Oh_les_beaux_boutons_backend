from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Custom user model with additional fields for NIRD swipe."""
    
    school_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Nom de l'établissement")
    school_type = models.CharField(
        max_length=50, 
        choices=[
            ('primaire', 'École Primaire'),
            ('college', 'Collège'),
            ('lycee', 'Lycée'),
            ('universite', 'Université'),
            ('autre', 'Autre'),
        ],
        blank=True, 
        null=True,
        verbose_name="Type d'établissement"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'

    def __str__(self):
        return self.email or self.username


class UserProfile(models.Model):
    """Extended profile for users."""
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    total_games_played = models.IntegerField(default=0)
    best_nird_score = models.IntegerField(default=0)
    total_points_earned = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Profil Utilisateur'
        verbose_name_plural = 'Profils Utilisateurs'

    def __str__(self):
        return f"Profil de {self.user}"
