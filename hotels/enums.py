# hotels/enums.py
from django.db import models


class RoomType(models.TextChoices):
    SINGLE = 'SINGLE', 'Single'
    DOUBLE = 'DOUBLE', 'Double'
    DELUXE = 'DELUXE', 'Deluxe'
    SUITE  = 'SUITE',  'Suite'


class BookingStatus(models.TextChoices):
    PENDING   = 'PENDING',   'Pending'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    CANCELLED = 'CANCELLED', 'Cancelled'
    