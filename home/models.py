from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.forms import ValidationError
from datetime import date
# Create your models here.

class Customer(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class Room(models.Model):
    room_types = [
        ('Deluxe',  'Deluxe'),
        ('Standard', 'Standard'),
        ('Suite', 'Suite'),
    ]
    name = models.CharField(max_length=50, unique=True, default=True)
    type = models.CharField(max_length=20, choices=room_types, default=True)
    #room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=True)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('booked', 'Booked'), ('maintenance', 'Maintenance')])
    def __str__(self):
        return f"{self.name}-{self.type}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def clean(self):
        # Kiểm tra ngày check-in/check-out hợp lệ
        if self.check_in_date < date.today():
            raise ValidationError("Check-in date must be today or later.")
        if self.check_out_date <= self.check_in_date:
            raise ValidationError("Check-out date must be after check-in date.")

        # Kiểm tra nếu phòng đã được đặt trong khoảng thời gian này
        overlapping_bookings = Booking.objects.filter(
            room=self.room,
            status='Confirmed',  # Chỉ kiểm tra các booking đã xác nhận
            check_in_date__lt=self.check_out_date,  # Booking có check-in trước ngày check-out mới
            check_out_date__gt=self.check_in_date   # Booking có check-out sau ngày check-in mới
        ).exclude(pk=self.pk)  # Loại trừ booking hiện tại nếu đang cập nhật
        if overlapping_bookings.exists():
            raise ValidationError(f"Room {self.room.name} is already booked for the selected dates.")

    def save(self, *args, **kwargs):
        # Gọi phương thức clean() để kiểm tra logic
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.id} for {self.customer.username} ({self.check_in_date} - {self.check_out_date})"
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('staff', 'Staff')])
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role})"








    

