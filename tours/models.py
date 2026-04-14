from django.db import models
from users.models import CustomUser


class Tour(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    name        = models.CharField(max_length=200)
    description = models.TextField()
    city        = models.CharField(max_length=100)
    destination = models.CharField(max_length=200)
    duration    = models.PositiveIntegerField(help_text="Duration in days")
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    max_people  = models.PositiveIntegerField(default=10)
    difficulty  = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    
    image       = models.ImageField(upload_to='tours/', null=True, blank=True)
    
    image_url   = models.URLField(max_length=500, null=True, blank=True)
    
    rating      = models.FloatField(default=0.0)
    includes    = models.TextField(blank=True)
    
    owner            = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='tours')
    created_at       = models.DateTimeField(auto_now_add=True)
    highlights       = models.TextField(blank=True, help_text="Why visit - bullet points separated by |")
    not_included     = models.TextField(blank=True, help_text="What is NOT included, separated by |")
    estrictions      = models.TextField(blank=True, help_text="Restrictions, separated by |")
    additional_info  = models.TextField(blank=True)

    def __str__(self):
        return self.name