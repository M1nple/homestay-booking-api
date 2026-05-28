from django.urls import path

from reviews.views.review_views import (
    CreateReviewView,
    MyReviewListView,
    RoomReviewListView
)

urlpatterns = [

    path(
        '',
        CreateReviewView.as_view()
    ),

    path(
        'my/',
        MyReviewListView.as_view()
    ),

    path(
        'rooms/<int:room_id>/',
        RoomReviewListView.as_view()
    ),
]