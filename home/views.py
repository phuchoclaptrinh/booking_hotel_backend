from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .permissions import IsEmployee
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Room, Booking
from .serializers import RoomSerializer, BookingSerializer
from django.core.exceptions import ValidationError
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here
class RoomListView(APIView):
    def get(self, request):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
class AvailableRoomListView(APIView):
    def get(self, request):
        rooms = Room.objects.filter(is_available=True)
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)
#class RoomHistoryViewSet(viewsets.ModelViewSet):
   # queryset = RoomHistory.objects.all()
    #serializer_class = RoomHistorySerializer
@method_decorator(csrf_exempt, name='dispatch')
class BookingCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Yêu cầu xác thực

    def post(self, request):
        # Kiểm tra nếu người dùng đã đăng nhập
        if not request.user.is_authenticated:
            return Response({'detail': 'User is not authenticated.'}, status=status.HTTP_401_UNAUTHORIZED)

        # Khởi tạo serializer với dữ liệu từ yêu cầu
        serializer = BookingSerializer(data=request.data, context={'request': request})

        # Kiểm tra tính hợp lệ của serializer và lưu
        if serializer.is_valid():
            serializer.save()
            booking = serializer.save(status='Confirmed')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Nếu không hợp lệ, trả về lỗi
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookingHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(customer=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
#class EmployeeViewSet(viewsets.ModelViewSet):
    #queryset = Employee.objects.all()
    #serializer_class = EmployeeSerializer

class RoomCreateView(CreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_class = [IsAuthenticated, IsEmployee]
class RoomDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_class = [IsAuthenticated, IsEmployee]
class CheckAvailableRoomsView(APIView):
    def get(self, request):
        check_in_date = request.query_params.get('check_in_date')
        check_out_date = request.query_params.get('check_out_date')

        if not check_in_date or not check_out_date:
            return Response({
                "detail": "Missing parameters. Please provide check_in_date and check_out_date."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra và chuyển đổi ngày tháng sang kiểu Date
        try:
            check_in_date = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({
                "detail": "Invalid date format. Expected format: YYYY-MM-DD."
            }, status=status.HTTP_400_BAD_REQUEST)

        # Lọc tất cả các phòng chưa được đặt trong khoảng thời gian này
        available_rooms = Room.objects.filter(
            is_available=True  # Chỉ lấy các phòng có sẵn
        ).exclude(
            id__in=Booking.objects.filter(
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date
            ).values('room')
        )  # Loại bỏ các phòng đã có booking trong khoảng thời gian

        # Kiểm tra xem có phòng nào còn trống không
        if not available_rooms.exists():
            return Response({
                "detail": "No rooms available for the selected dates."
            }, status=status.HTTP_404_NOT_FOUND)

        # Trả về thông tin các phòng còn trống
        serializer = RoomSerializer(available_rooms, many=True)
        return Response({
            "available_rooms": serializer.data
        })
class RoleCheckView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            return Response({'role': 'employee'})
        else:
            return Response({'role': 'customer'})