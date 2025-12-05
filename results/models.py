from django.db import models
from django.conf import settings


class GameResult(models.Model):
    """Stores the results of a completed game session."""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='game_results',
        null=True,
        blank=True
    )
    session_id = models.CharField(max_length=100, blank=True)  # For anonymous users
    
    # Scores
    nird_score = models.IntegerField(verbose_name="Score NIRD (%)")
    total_points = models.IntegerField(verbose_name="Points totaux")
    
    # Pillar scores
    inclusion_score = models.IntegerField(default=0)
    responsabilite_score = models.IntegerField(default=0)
    durabilite_score = models.IntegerField(default=0)
    
    # Savings
    total_savings_euros = models.IntegerField(default=0)
    total_savings_co2 = models.IntegerField(default=0)
    
    # Metadata
    cards_played = models.IntegerField(default=0)
    correct_choices = models.IntegerField(default=0)
    
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Résultat de jeu'
        verbose_name_plural = 'Résultats de jeux'
        ordering = ['-completed_at']
    
    def __str__(self):
        user_str = self.user.username if self.user else f"Anonyme ({self.session_id[:8]})"
        return f"{user_str} - Score: {self.nird_score}%"


class GameChoice(models.Model):
    """Individual choice made during a game."""
    
    game_result = models.ForeignKey(GameResult, on_delete=models.CASCADE, related_name='choices')
    card_id = models.CharField(max_length=50)
    card_name = models.CharField(max_length=100)
    card_type = models.CharField(max_length=20)  # big-tech or nird
    accepted = models.BooleanField()
    points_earned = models.IntegerField()
    timestamp = models.DateTimeField()
    
    class Meta:
        verbose_name = 'Choix de jeu'
        verbose_name_plural = 'Choix de jeux'
        ordering = ['timestamp']
    
    def __str__(self):
        action = "Gardé" if self.accepted else "Remplacé"
        return f"{self.card_name}: {action}"


class WrongAnswer(models.Model):
    """Tracks wrong answers for personalized recommendations."""
    
    game_result = models.ForeignKey(GameResult, on_delete=models.CASCADE, related_name='wrong_answers')
    card_id = models.CharField(max_length=50)
    card_name = models.CharField(max_length=100)
    card_type = models.CharField(max_length=20)
    alternative_name = models.CharField(max_length=100, blank=True)
    reason = models.TextField()  # Why this was wrong
    recommendation = models.TextField()  # What to do instead
    
    class Meta:
        verbose_name = 'Mauvaise réponse'
        verbose_name_plural = 'Mauvaises réponses'
    
    def __str__(self):
        return f"{self.card_name} - {self.card_type}"
