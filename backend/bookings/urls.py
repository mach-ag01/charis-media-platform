from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, ProductionTaskViewSet, dashboard
router = DefaultRouter()
router.register("bookings", BookingViewSet, basename="booking")
router.register("tasks", ProductionTaskViewSet, basename="task")
urlpatterns = [path("dashboard/", dashboard), path("", include(router.urls))]
