from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = Review.objects.all()
        if self.request.query_params.get('hotel'):
            qs = qs.filter(hotel=self.request.query_params['hotel'])
        if self.request.query_params.get('restaurant'):
            qs = qs.filter(restaurant=self.request.query_params['restaurant'])
        if self.request.query_params.get('event'):
            qs = qs.filter(event=self.request.query_params['event'])
        return qs