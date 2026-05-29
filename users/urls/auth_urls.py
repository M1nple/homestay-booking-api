from django.urls import path
from ..views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),  # Thêm đường dẫn cho logout
    path('me/', MeView.as_view()),  # Thêm đường dẫn cho lấy thông tin người dùng
    path('update/', UpdateUserView.as_view()),  # Thêm đường dẫn cho cập nhật thông tin người dùng
    # path('host-request/', HostRequestView.as_view()),  # Thêm đường dẫn cho gửi yêu cầu trở thành host
    path('verify-email/',VerifyEmailView.as_view()),
    path('resend-otp/',ResendOTPView.as_view(),name='resend-otp'),
    ]