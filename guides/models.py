from django.db import models

class Guide(models.Model):
    LANGUAGE_CHOICES = [
        ('ru', 'Russian'),
        ('en', 'English'),
        ('ky', 'Kyrgyz'),
        ('zh', 'Chinese'),
        ('de', 'German'),
        ('fr', 'French'),
    ]
    
    SPECIALIZATION_CHOICES = [
        ('trekking', 'Trekking'),
        ('cultural', 'Cultural'),
        ('history', 'History'),
        ('nomad', 'Nomad Experience'),
        ('photography', 'Photography'),
        ('adventure', 'Adventure'),
    ]

    name = models.CharField(max_length=200)
    bio = models.TextField()
    photo = models.URLField(blank=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    languages = models.CharField(max_length=200)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATION_CHOICES)
    location = models.CharField(max_length=200)
    experience_years = models.IntegerField(default=1)
    rating = models.FloatField(default=5.0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
