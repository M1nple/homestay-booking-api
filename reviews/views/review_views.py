from django.db.models import Avg

from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticated
)
from rooms.models import Room
from reviews.models import Review
from reviews.serializers.review_serializers import (
    ReviewSerializer,
    CreateReviewSerializer
)


# =====================
# Create Review
# =====================

class CreateReviewView(
    generics.CreateAPIView
):

    serializer_class = (
        CreateReviewSerializer
    )

    permission_classes = [
        IsAuthenticated
    ]


# =====================
# My Reviews
# =====================

class MyReviewListView(
    generics.ListAPIView
):

    serializer_class = ReviewSerializer

    permission_classes = [
        IsAuthenticated
    ]

    def get_queryset(self):

        return Review.objects.filter(
            user=self.request.user
        )


# =====================
# Room Reviews
# =====================

class RoomReviewListView(
    generics.ListAPIView
):

    serializer_class = ReviewSerializer

    def get_queryset(self):

        room_id = self.kwargs['room_id']

        return Review.objects.filter(
            room_id=room_id
        )
    
