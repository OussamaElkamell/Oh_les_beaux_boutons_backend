from django.db import models


class Pillar(models.Model):
    """NIRD pillars: Inclusion, Responsabilité, Durabilité."""
    
    PILLAR_CHOICES = [
        ('inclusion', 'Inclusion'),
        ('responsabilite', 'Responsabilité'),
        ('durabilite', 'Durabilité'),
    ]
    
    name = models.CharField(max_length=50, choices=PILLAR_CHOICES, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, blank=True)  # Emoji
    
    class Meta:
        verbose_name = 'Pilier NIRD'
        verbose_name_plural = 'Piliers NIRD'
    
    def __str__(self):
        return self.get_name_display()


class Category(models.Model):
    """Technology categories."""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TechnologyCard(models.Model):
    """Technology card for the NIRD swipe game."""
    
    TYPE_CHOICES = [
        ('big-tech', 'Big Tech'),
        ('nird', 'NIRD'),
    ]
    
    # Basic info
    card_id = models.CharField(max_length=50, unique=True, verbose_name="ID Carte")
    name = models.CharField(max_length=100, verbose_name="Nom")
    card_type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Type")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='cards')
    pillar = models.CharField(
        max_length=20, 
        choices=Pillar.PILLAR_CHOICES, 
        verbose_name="Pilier"
    )
    description = models.TextField(verbose_name="Description")
    icon = models.CharField(max_length=10, verbose_name="Icône")  # Emoji
    
    # Stats
    cost = models.CharField(max_length=50, verbose_name="Coût")
    co2 = models.CharField(max_length=50, verbose_name="Impact CO2")
    data_location = models.CharField(max_length=100, verbose_name="Localisation données")
    
    # Alternative (for NIRD cards)
    alternative = models.ForeignKey(
        'self', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='alternatives',
        verbose_name="Alternative"
    )
    
    # Savings (for NIRD cards)
    savings_euros = models.IntegerField(default=0, verbose_name="Économies €")
    savings_co2_kg = models.IntegerField(default=0, verbose_name="Économies CO2 (kg)")
    
    # Metadata
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Carte Technologie'
        verbose_name_plural = 'Cartes Technologies'
        ordering = ['category', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_card_type_display()})"
