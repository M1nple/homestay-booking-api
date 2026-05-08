from django.urls import path

from rooms.views.host_views import RoomViewSet


room_list = RoomViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

room_detail = RoomViewSet.as_view({
    'get': 'retrieve',
    'patch': 'partial_update',
    'put': 'update',
    'delete': 'destroy',
})


urlpatterns = [

    path(
        'homestays/<int:homestay_id>/rooms/',
        room_list,
        name='room-list',
    ),

    path(
        'homestays/<int:homestay_id>/rooms/<int:pk>/',
        room_detail,
        name='room-detail',
    ),
]