#from rest_framework import generics
#from .models import Hotel
#from .serializers import HotelSerializer,RoomSerializer
#from .models import Room
#
##Hotel 
#class HotelListCreateView(generics.ListCreateAPIView):
#    queryset = Hotel.objects.all()
#    serializer_class = HotelSerializer
#    
#
#
#
#
#class HotelListView(generics.ListAPIView):
#    """
#    GET /api/hotels/
#    List all hotels.
#    """
#    queryset = Hotel.objects.all()
#    serializer_class = HotelSerializer
#    filterset_fields = ['city', 'star_rating']   # optional filtering
#
#
#class HotelDetailView(generics.RetrieveAPIView):
#    """
#    GET /api/hotels/{id}/
#    Retrieve a single hotel by ID.
#    """
#    queryset = Hotel.objects.all()
#    serializer_class = HotelSerializer
#
#
#    # ROOM
## ─────────────────────────────────────────────
#class RoomListCreateView(generics.ListCreateAPIView):
#    """
#    GET  /api/rooms/   → list rooms (supports ?hotel=&room_type=&min_price=&max_price=)
#    POST /api/rooms/   → create a room
#    """
#    queryset = Room.objects.select_related('hotel').all()
#    serializer_class = RoomSerializer
#    
#
#
#class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
#    """
#    GET/PUT/PATCH/DELETE /api/rooms/{id}/
#    """
#    queryset = Room.objects.select_related('hotel').all()
#    serializer_class = RoomSerializer
#
#class HotelRoomsListView(generics.ListAPIView):
#    """
#    GET /api/hotels/{id}/rooms/
#    List all rooms belonging to a specific hotel.
#    """
#    serializer_class = RoomSerializer
#
#    def get_queryset(self):
#        hotel_id = self.kwargs['pk']
#        # Raises 404 if the hotel doesn't exist — clean error for the client
#        hotel = get_object_or_404(Hotel, pk=hotel_id)
#        return Room.objects.filter(hotel=hotel).select_related('hotel')





from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
    OpenApiResponse,
)
from drf_spectacular.types import OpenApiTypes

from .models import Hotel, Room
from .serializers import HotelSerializer, RoomSerializer



# ─────────────────────────────────────────────
# HOTEL
# ─────────────────────────────────────────────
@extend_schema_view(
    list=extend_schema(
        tags=['Hotels'],
        summary="List all hotels",
        description="Returns a list of hotels. Supports filtering by city and star rating.",
        parameters=[
            OpenApiParameter(
                name='city',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter by city name (exact match).",
            ),
            OpenApiParameter(
                name='min_stars',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Minimum star rating (1–5).",
            ),
            OpenApiParameter(
                name='max_stars',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Maximum star rating (1–5).",
            ),
        ],
        responses={200: HotelSerializer(many=True)},
    ),
    create=extend_schema(
        tags=['Hotels'],
        summary="Create a hotel",
        description="Create a new hotel. `star_rating` must be between 1 and 5.",
        request=HotelSerializer,
        responses={
            201: HotelSerializer,
            400: OpenApiResponse(description="Invalid input (e.g., star_rating out of range)."),
        },
        examples=[
            OpenApiExample(
                "Valid hotel",
                value={
                    "name": "Grand Hotel",
                    "description": "Luxury hotel downtown",
                    "address": "123 Main St",
                    "city": "Tehran",
                    "star_rating": 4,
                },
                request_only=True,
            ),
        ],
    ),
)
class HotelListCreateView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
   


@extend_schema_view(
    retrieve=extend_schema(
        tags=['Hotels'],
        summary="Get hotel details",
        responses={200: HotelSerializer, 404: OpenApiResponse(description="Hotel not found.")},
    ),
    update=extend_schema(tags=['Hotels'], summary="Update hotel (full)"),
    partial_update=extend_schema(tags=['Hotels'], summary="Update hotel (partial)"),
    destroy=extend_schema(tags=['Hotels'], summary="Delete hotel"),
)
class HotelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


# ─────────────────────────────────────────────
# HOTEL → ROOMS
# ─────────────────────────────────────────────
@extend_schema(
    tags=['Hotels'],
    summary="List rooms of a specific hotel",
    description="Returns all rooms belonging to the hotel with the given ID.",
    parameters=[
        OpenApiParameter(
            name='id',
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Hotel ID",
        ),
    ],
    responses={
        200: RoomSerializer(many=True),
        404: OpenApiResponse(description="Hotel not found."),
    },
)
class HotelRoomsListView(generics.ListAPIView):
    serializer_class = RoomSerializer

    def get_queryset(self):
        hotel = get_object_or_404(Hotel, pk=self.kwargs['pk'])
        return Room.objects.filter(hotel=hotel).select_related('hotel')


# ─────────────────────────────────────────────
# ROOM
# ─────────────────────────────────────────────
@extend_schema_view(
    list=extend_schema(
        tags=['Rooms'],
        summary="List rooms",
        parameters=[
            OpenApiParameter('hotel', OpenApiTypes.INT, OpenApiParameter.QUERY,
                             description="Filter by hotel ID"),
            OpenApiParameter('room_type', OpenApiTypes.STR, OpenApiParameter.QUERY,
                             description="SINGLE | DOUBLE | DELUXE | SUITE"),
            OpenApiParameter('min_price', OpenApiTypes.DECIMAL, OpenApiParameter.QUERY),
            OpenApiParameter('max_price', OpenApiTypes.DECIMAL, OpenApiParameter.QUERY),
        ],
    ),
    create=extend_schema(
        tags=['Rooms'],
        summary="Create a room",
        description="`room_type` must be one of: SINGLE, DOUBLE, DELUXE, SUITE.",
    ),
)
class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.select_related('hotel').all()
    serializer_class = RoomSerializer
  


@extend_schema_view(
    retrieve=extend_schema(tags=['Rooms'], summary="Get room details"),
    update=extend_schema(tags=['Rooms'], summary="Update room (full)"),
    partial_update=extend_schema(tags=['Rooms'], summary="Update room (partial)"),
    destroy=extend_schema(tags=['Rooms'], summary="Delete room"),
)
class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.select_related('hotel').all()
    serializer_class = RoomSerializer

class HotelRoomsListView(generics.ListAPIView):
    """
    GET /api/hotels/{id}/rooms/
    Returns all rooms belonging to the given hotel.
    """
    serializer_class = RoomSerializer

    def get_queryset(self):
        hotel = get_object_or_404(Hotel, pk=self.kwargs['pk'])
        return Room.objects.filter(hotel=hotel).select_related('hotel')