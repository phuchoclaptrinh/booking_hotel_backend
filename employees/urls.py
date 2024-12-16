from django.urls import path 
from rest_framework.routers import DefaultRouter
from users.views import(
    RegisterView, LoginView
)
from home.views import (
    RoomListView, AvailableRoomListView, BookingCreateView, 
    BookingHistoryView, RoomCreateView, RoomDetailView, RoleCheckView
)
urlpatterns = [
    path('rooms/', RoomListView.as_view(), name='room-list'),
    path('rooms/available/', AvailableRoomListView.as_view(), name='available-room-list'),
    path('bookings/', BookingCreateView.as_view(), name='create-booking'),
    path('bookings/history/', BookingHistoryView.as_view(), name='booking-history'),

    path('rooms/add/', RoomCreateView.as_view(), name='add-room'),
    path('rooms/<int:pk>', RoomDetailView.as_view(), name='room-detail'),
    path('role/', RoleCheckView.as_view(), name='role-check'),
    path('login/',LoginView.as_view(), name='login'),
    path('register/',LoginView.as_view(), name='register'),
    ]
