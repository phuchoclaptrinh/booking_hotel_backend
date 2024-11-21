from rest_framework import viewsets
from .models import Room, RoomType, RoomHistory, Booking, Employee
from .serializers import RoomSerializer, RoomTypeSerializer, RoomHistorySerializer, BookingSerializer, EmployeeSerializer # type: ignore
# Create your views here
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
class RoomTypeViewSet(viewsets.ModelViewSet):
    queryset = RoomType.objects.all()
    serializer_class = RoomTypeSerializer
class RoomHistoryViewSet(viewsets.ModelViewSet):
    queryset = RoomHistory.objects.all()
    serializer_class = RoomHistorySerializer
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer