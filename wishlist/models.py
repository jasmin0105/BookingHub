from django.db import models
from users.models import CustomUser


class WishlistItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlist')
    hotel = models.ForeignKey('hotels.Hotel', null=True, blank=True, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('restaurants.Restaurant', null=True, blank=True, on_delete=models.CASCADE)
    event = models.ForeignKey('events.Event', null=True, blank=True, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = []

    def __str__(self):
        item = self.hotel or self.restaurant or self.event
        return f"{self.user.email} → {item}"