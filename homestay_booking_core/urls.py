"""
URL configuration for homestay_booking_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include 
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


urlpatterns = [
# Admin site
    path('admin/', admin.site.urls),

# API swagger documentation (docs)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema')),

# API endpoints

    #admin API endpointss
    path('api/admin/', include('users.urls.admin_urls')), # thêm đường dẫn cho app users

    #auth API endpoints
    path('api/auth/', include('users.urls.auth_urls')), # thêm đường dẫn cho app users

    # locations API endpoints
    path('api/locations/', include('locations.urls')), # thêm đường dẫn cho app locations

    # host API endpoints
    path('api/host/', include('homestays.urls.host_urls')), # thêm đường dẫn cho app homestays
    path('api/host/', include('rooms.urls.host_urls')), # thêm đường dẫn cho app rooms
    path('api/host/', include('bookings.urls.host_urls')), # thêm đường dẫn cho app bookings
    
    # customer API endpoints
    path('api/', include('homestays.urls.public_urls')), # thêm đường dẫn cho app homestays
    path('api/', include('rooms.urls.public_urls')), # thêm đường dẫn cho app rooms
    path('api/customer/', include('bookings.urls.customer_urls')), # thêm đường dẫn cho app bookings
    path('api/customer/', include('users.urls.customer_urls')), # thêm đường dẫn cho app users

    # payment API endpoints
    path('api/payments/', include('payments.urls')), # thêm đường dẫn cho app payments
]

