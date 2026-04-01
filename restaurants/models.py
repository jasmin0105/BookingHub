from django.db import models
from django.conf import settings

class Restaurant(models.Model):
    owner        = models.ForeignKey(
                       settings.AUTH_USER_MODEL,
                       on_delete=models.SET_NULL,
                       null=True, blank=True,
                       related_name='restaurants'
                   )
    name         = models.CharField(max_length=200)
    description  = models.TextField(blank=True)
    address      = models.CharField(max_length=500, blank=True)
    city         = models.CharField(max_length=100)
    cuisine_type = models.CharField(max_length=100, blank=True)
    rating       = models.FloatField(default=0)
    image        = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
