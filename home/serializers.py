from django.forms import ValidationError
from rest_framework import serializers
from .models import Customer, Room, Booking, Employee

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


from rest_framework import serializers
from .models import Booking, Room
from django.core.exceptions import ValidationError

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Thiết lập khách hàng là người dùng hiện tại
            validated_data['customer'] = request.user
        else:
            raise ValidationError("User is not authenticated.")
        
        # Lưu và trả về đối tượng booking
        return super().create(validated_data)



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

        