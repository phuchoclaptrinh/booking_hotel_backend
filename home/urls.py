from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, RoomTypeViewSet, RoomHistoryViewSet, BookingViewSet, EmployeeViewSet
router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'room_type', RoomTypeViewSet)
router.register(r'room_history', RoomHistoryViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'employees', EmployeeViewSet)

urlpatterns = [
    path('',include(router.urls)),
    ]

