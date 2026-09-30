from django.db import models
from hotels.enums import BookingStatus
from hotels.models import Hotel,Room
# Create your models here.


from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Booking(models.Model):
    user_id = models.PositiveIntegerField(
        help_text="ID of the user in the Auth Service"
    )


    room = models.ForeignKey(
        'hotels.Room',
        on_delete=models.PROTECT,   # don't allow deleting a room with active bookings
        related_name='bookings',
    )

    check_in = models.DateField()
    check_out = models.DateField()
    number_of_guests = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message="At least 1 guest required."),
            MaxValueValidator(10, message="Maximum 10 guests."),
        ],
    )

    
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(
        max_length=10,
        choices=BookingStatus.choices,
        default=BookingStatus.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bookings'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['status']),
            models.Index(fields=['check_in', 'check_out']),
        ]

    def __str__(self):
        return f"Booking #{self.id} — user {self.user_id} — {self.status}"


    