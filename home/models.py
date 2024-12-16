from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.forms import ValidationError
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
    #room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=True)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('booked', 'Booked'), ('maintenance', 'Maintenance')])
    def __str__(self):
        return f"{self.name}-{self.type}"


class Booking(models.Model):
    status_choices = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length=20, choices=status_choices, default='Pending')

    def save(self, *args, **kwargs):
        # Kiểm tra nếu phòng còn trống
        if self.room.status != 'available':
            raise ValidationError(f"Room {self.room.name} is not available.")
        
        # Cập nhật trạng thái phòng sau khi tạo booking
        if self.status == 'Confirmed':
            self.room.status = 'booked'
        elif self.status == 'Cancelled' and self.room.status == 'booked':
            self.room.status = 'available'

        # Lưu thông tin phòng và đối tượng booking
        self.room.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.id} for {self.customer.username}"

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('staff', 'Staff')])
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role})"






    

