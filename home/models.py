from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class RoomType(models.Model):
    type_name = models.CharField(max_length=100)
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.type_name


class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    price_per_night = models.TextField()
    description = models.TextField(default='No description')
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('booked', 'Booked'), ('maintenance', 'Maintenance')])
    def __str__(self):
        return f"Room {self.id}-{self.room_type.type_name}"


class Booking(models.Model):
    customer_name = models.CharField(max_length=255)
    customer_contact = models.CharField(max_length=255)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=[('pending', 'Pending'),('confirmed', 'Confirmed'), ('cancelled', 'Cancelled')]
    )
    def __str__(self):
        return f"Booking {self.id} for {self.customer_name}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=[('admin', 'Admin'), ('staff', 'Staff')])
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return f"Employee {self.name} ({self.role})"

class RoomHistory(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    check_in_date = models.DateField()
    check_out_name = models.DateField()
    status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('cancelled', 'Cancelled')])
    def __str__(self):
        return f"History {self.id} for Room {self.room.id}-{self.status}"

