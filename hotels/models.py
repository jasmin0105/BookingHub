from django.db import models
from django.conf import settings


class Hotel(models.Model):
    owner           = models.ForeignKey(
                          settings.AUTH_USER_MODEL,
                          on_delete=models.SET_NULL,
                          null=True, blank=True,
                          related_name='hotels'
                      )
    name            = models.CharField(max_length=200)
    description     = models.TextField()
    address         = models.CharField(max_length=500)
    city            = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    rating          = models.FloatField(default=0)
    image           = models.ImageField(upload_to='hotels/', blank=True, null=True)
    available_rooms = models.IntegerField(default=1)
    created_at      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
