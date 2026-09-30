from django.db import models

# Create your models here.

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .enums import RoomType

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)

    star_rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Star rating must be at least 1."),
            MaxValueValidator(5, message="Star rating cannot exceed 5."),
        ],
        help_text="Rating from 1 to 5",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hotels'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['star_rating']),
        ]

    def __str__(self):
        return f"{self.name} ({self.city}) — {self.star_rating}★"



from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .enums import RoomType


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    address = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    star_rating = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Star rating must be at least 1."),
            MaxValueValidator(5, message="Star rating cannot exceed 5."),
        ],
        help_text="Rating from 1 to 5",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hotels'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['city']),
            models.Index(fields=['star_rating']),
        ]

    def __str__(self):
        return f"{self.name} ({self.city}) — {self.star_rating}★"


class Room(models.Model):
    # 👇 ForeignKey creates `hotel_id` automatically in the DB
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE, # if the hotel (parent) will be deleted 
        related_name='rooms',
    )

    room_number = models.CharField(max_length=20)
    room_type = models.CharField(
        max_length=10,
        choices=RoomType.choices,
        default=RoomType.SINGLE,
    )
    price_per_night = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0, message="Price cannot be negative.")],
    )
    capacity = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="Capacity must be at least 1."),
            MaxValueValidator(10, message="Capacity cannot exceed 10."),
        ],
        help_text="Number of guests",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'rooms'
        ordering = ['hotel', 'room_number']
        # 👇 room_number must be unique *within* a hotel
        constraints = [
            models.UniqueConstraint(
                fields=['hotel', 'room_number'],
                name='unique_room_per_hotel',
            ),
        ]
        indexes = [
            models.Index(fields=['hotel']),
            models.Index(fields=['room_type']),
            models.Index(fields=['price_per_night']),
        ]

    def __str__(self):
        return f"Room {self.room_number} — {self.get_room_type_display()} @ {self.hotel.name}"
    