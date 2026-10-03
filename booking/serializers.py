from rest_framework import serializers
from datetime import date

from .models import Booking
from hotels.enums import BookingStatus
from hotels.serializers import RoomMiniSerializer


class BookingSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(
        choices=BookingStatus.choices,
        required=False,
        default=BookingStatus.PENDING,
    )

    class Meta:
        model = Booking
        fields = [
            'id', 'user_id', 'room',
            'check_in', 'check_out', 'number_of_guests',
            'price_per_night', 'total_price',
            'status', 'created_at', 'updated_at',
        ]
        read_only_fields = [
            'id', 'user_id',
            'price_per_night', 'total_price',
            'created_at', 'updated_at',
        ]

    def validate(self, attrs):
        check_in = attrs.get('check_in')
        check_out = attrs.get('check_out')
        room = attrs.get('room')
        guests = attrs.get('number_of_guests')

        # ── 1) check_in must be today or later
        if check_in and check_in < date.today():
            raise serializers.ValidationError({
                'check_in': "Check-in cannot be in the past."
            })

        # ── 2) check_out must be after check_in
        if check_in and check_out and check_out <= check_in:
            raise serializers.ValidationError({
                'check_out': "Check-out must be after check-in."
            })

        # ── 3) capacity check
        if room and guests and guests > room.capacity:
            raise serializers.ValidationError({
                'number_of_guests': (
                    f"This room holds at most {room.capacity} guests."
                )
            })

        # ── 4) room availability for the period
        if room and check_in and check_out:
            qs = Booking.objects.filter(
                room=room,
                status__in=[BookingStatus.PENDING, BookingStatus.CONFIRMED],
                check_in__lt=check_out,     # existing starts before new ends
                check_out__gt=check_in,     # existing ends after new starts
            )
            # when updating, exclude self
            if self.instance:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise serializers.ValidationError({
                    'room': (
                        "This room is already booked for the selected period."
                    )
                })

        return attrs

    def create(self, validated_data):
        room = validated_data['room']
        check_in = validated_data['check_in']
        check_out = validated_data['check_out']

        # ── Compute nights & prices
        nights = (check_out - check_in).days
        validated_data['price_per_night'] = room.price_per_night
        validated_data['total_price'] = room.price_per_night * nights

        return super().create(validated_data)


class BookingReadSerializer(serializers.ModelSerializer):
    """Nested read serializer."""
    room = RoomMiniSerializer(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'room',
            'check_in', 'check_out', 'number_of_guests',
            'price_per_night', 'total_price',
            'status', 'created_at', 'updated_at',
        ]