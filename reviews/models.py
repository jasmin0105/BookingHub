from django.db import models
from users.models import CustomUser

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reviews')
    hotel = models.ForeignKey('hotels.Hotel', null=True, blank=True, on_delete=models.CASCADE, related_name='reviews')
    restaurant = models.ForeignKey('restaurants.Restaurant', null=True, blank=True, on_delete=models.CASCADE, related_name='reviews')
    event = models.ForeignKey('events.Event', null=True, blank=True, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i,i) for i in range(1,6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.rating}★"