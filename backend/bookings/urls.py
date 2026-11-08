
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    BookingViewSet,
    ProductionTaskViewSet,
    dashboard,
)

from .auth_views import (
    CustomerRegistrationView,
    LoginView,
    RefreshTokenView,
    CurrentUserView,
    StaffAccountCreateView,
)

router = DefaultRouter()

router.register(
    "bookings",
    BookingViewSet,
    basename="booking",
)

router.register(
    "tasks",
    ProductionTaskViewSet,
    basename="task",
)

urlpatterns = [
    # Authentication
    path(
        "auth/register/",
        CustomerRegistrationView.as_view(),
        name="customer-register",
    ),
    path(
        "auth/login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "auth/refresh/",
        RefreshTokenView.as_view(),
        name="token-refresh",
    ),
    path(
        "auth/me/",
        CurrentUserView.as_view(),
        name="current-user",
    ),
    path(
        "auth/staff/create/",
        StaffAccountCreateView.as_view(),
        name="staff-create",
    ),

    # Application endpoints
    path("dashboard/", dashboard),
    path("", include(router.urls)),
]
