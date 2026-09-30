from rest_framework import serializers
from .models import Hotel, Room
from .enums import RoomType, BookingStatus

# ─────────────────────────────────────────────
# HOTEL
# ─────────────────────────────────────────────
class HotelSerializer(serializers.ModelSerializer):
    star_rating = serializers.IntegerField(min_value=1, max_value=5)

    class Meta:
        model = Hotel
        fields = [
            'id', 'name', 'description', 'address', 'city',
            'star_rating', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


# ─────────────────────────────────────────────
# ROOM
# ─────────────────────────────────────────────
class RoomSerializer(serializers.ModelSerializer):
    # 👇 dropdown in Swagger: SINGLE / DOUBLE / DELUXE / SUITE
    room_type = serializers.ChoiceField(choices=RoomType.choices)

    class Meta:
        model = Room
        fields = [
            'id', 'hotel', 'room_number', 'room_type',
            'price_per_night', 'capacity',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class RoomMiniSerializer(serializers.ModelSerializer):
    """Short read-only Room representation used by the booking app."""
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'room_type', 'price_per_night', 'capacity']