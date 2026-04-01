from django.db import models
from django.conf import settings

class Event(models.Model):
    owner       = models.ForeignKey(
                      settings.AUTH_USER_MODEL,
                      on_delete=models.SET_NULL,
                      null=True, blank=True,
                      related_name='events'
                  )
    name        = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    city        = models.CharField(max_length=100)
    venue       = models.CharField(max_length=255, blank=True)
    date        = models.DateTimeField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    image       = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
