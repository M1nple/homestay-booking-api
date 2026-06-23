from django.urls import path
from admins.views.user_views import  AdminUserListView
from admins.views.homestay_views import AdminHomestayListView
from admins.views.booking_views import AdminBookingListView
from admins.views.payment_views import AdminPaymentListView, ApproveRefundAPIView
from admins.views.dashboard_views import AdminDashboardView
from users.views.admin_views import HostRequestViewSet


urlpatterns = [

    path(
        'dashboard/',
        AdminDashboardView.as_view()
    ),

    path(
        'users/',
        AdminUserListView.as_view()
    ),

    path(
        'homestays/',
        AdminHomestayListView.as_view()
    ),

    path(
        'bookings/',
        AdminBookingListView.as_view()
    ),

    path(
        'payments/',
        AdminPaymentListView.as_view()
    ),

    path(
    "bookings/<int:pk>/approve-refund/",
    ApproveRefundAPIView.as_view(),
    name="approve-refund"
    ),
    

]