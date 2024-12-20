from django.forms import ValidationError
from rest_framework import serializers
from .models import Customer, Room, Booking, Employee
from datetime import date


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'



class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def validate(self, data):
        # Kiểm tra logic ngày
        if data['check_in_date'] < date.today():
            raise serializers.ValidationError({
                "check_in_date": "Check-in date must be today or later."
            })
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError({
                "check_out_date": "Check-out date must be after check-in date."
            })

        # Kiểm tra xung đột đặt phòng (chỉ nếu status là Confirmed)
        if data['status'] == 'Confirmed':
            overlapping_bookings = Booking.objects.filter(
                room=data['room'],
                status='Confirmed',
                check_in_date__lt=data['check_out_date'],
                check_out_date__gt=data['check_in_date']
            )
            if overlapping_bookings.exists():
                conflicting_booking = overlapping_bookings.first()
                raise serializers.ValidationError({
                    "room": f"The room '{data['room'].name}' is already booked for the selected dates "
                            f"({conflicting_booking.check_in_date} to {conflicting_booking.check_out_date})."
                })

        return data

    def validate_check_in_date(self, value):
        """ Kiểm tra ngày check-in hợp lệ """
        if value < date.today():
            raise serializers.ValidationError("Check-in date must be today or later.")
        return value

    def validate_check_out_date(self, value):
        """ Kiểm tra ngày check-out hợp lệ """
        check_in_date = self.initial_data.get('check_in_date')
        # Chuyển đổi check_in_date từ chuỗi thành datetime.date nếu cần
        if isinstance(check_in_date, str):
            check_in_date = date.fromisoformat(check_in_date)
        if check_in_date and value <= check_in_date:
            raise serializers.ValidationError("Check-out date must be after check-in date.")
        return value


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'room', 'check_in_date', 'check_out_date', 'status']  # Chọn các trường cần trả về

    def to_representation(self, instance):
        """
        Tùy chỉnh cách dữ liệu được trả về.
        Ví dụ: có thể thêm tên phòng vào thay vì chỉ trả về id.
        """
        representation = super().to_representation(instance)
        representation['room_name'] = instance.room.name  # Thêm tên phòng vào kết quả
        return representation

        