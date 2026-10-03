#from rest_framework import generics
#from rest_framework.permissions import IsAuthenticated
#from drf_spectacular.utils import extend_schema, extend_schema_view
#from rest_framework_simplejwt.authentication import JWTAuthentication
#
#from .models import Booking
#from .serializers import BookingSerializer, BookingReadSerializer
#
#from .permissions import HasServiceToken
#from .tasks import send_booking_notification
#
#
#@extend_schema_view(
#    list=extend_schema(tags=['Bookings'], summary="List bookings"),
#    create=extend_schema(tags=['Bookings'], summary="Create a booking"),
#)
#class BookingListCreateView(generics.ListCreateAPIView):
#    """
#    GET  /api/bookings/   → list the current user's bookings
#    POST /api/bookings/   → create a booking for the current user
#    """
#    queryset = Booking.objects.select_related('room').all()
#
#    authentication_classes = [JWTAuthentication]
#    permission_classes = [IsAuthenticated]
#   
#
#
#    def get_serializer_class(self):
#        return BookingSerializer if self.request.method == 'POST' else BookingReadSerializer
#
#    def get_queryset(self):
#        return Booking.objects.filter(
#            user_id=self.request.user.id
#        ).select_related('room')
#
#    def perform_create(self, serializer):
#        booking = serializer.save(user_id=self.request.user.id)
#        send_booking_notification.delay(booking.id, booking.user_id, event='created')
#
#
#@extend_schema_view(
#    retrieve=extend_schema(tags=['Bookings'], summary="Get booking details"),
#    update=extend_schema(tags=['Bookings'], summary="Update booking"),
#    partial_update=extend_schema(tags=['Bookings'], summary="Partial update booking"),
#    destroy=extend_schema(tags=['Bookings'], summary="Cancel booking"),
#)
#class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
#    """
#    GET    /api/bookings/{id}/
#    PUT    /api/bookings/{id}/
#    PATCH  /api/bookings/{id}/
#    DELETE /api/bookings/{id}/
#    """
#    queryset = Booking.objects.select_related('room').all()
#    serializer_class = BookingSerializer
#    permission_classes = [IsAuthenticated, HasServiceToken]
#
#    def get_queryset(self):
#        return Booking.objects.filter(
#            user_id=self.request.user.id
#        ).select_related('room')
#
#    def perform_update(self, serializer):
#        booking = serializer.save()
#        if booking.status == 'CONFIRMED':
#            send_booking_notification.delay(booking.id, booking.user_id, event='confirmed')
#        elif booking.status == 'CANCELLED':
#            send_booking_notification.delay(booking.id, booking.user_id, event='cancelled')


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view

from .models import Booking
from .serializers import BookingSerializer, BookingReadSerializer

from .permissions import HasServiceToken
from .tasks import send_booking_notification


@extend_schema_view(
    list=extend_schema(tags=['Bookings'], summary="List the current user's bookings"),
    create=extend_schema(tags=['Bookings'], summary="Create a booking"),
)
class BookingListCreateView(generics.ListCreateAPIView):  
    queryset = Booking.objects.all()
    
    # 👇 custom JWT permission 
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return BookingSerializer if self.request.method == 'POST' else BookingReadSerializer

    def get_queryset(self):
        # 👇 request.user.id comes from HasValidJWT
        return Booking.objects.filter(
            user_id=self.request.user.id
        ).select_related('room')

    def perform_create(self, serializer):
        booking = serializer.save(user_id=self.request.user.id)
        send_booking_notification.delay(booking.id, booking.user_id, event='created')


@extend_schema_view(
    retrieve=extend_schema(tags=['Bookings'], summary="Get booking details"),
    update=extend_schema(tags=['Bookings'], summary="Update booking"),
    partial_update=extend_schema(tags=['Bookings'], summary="Partial update"),
    destroy=extend_schema(tags=['Bookings'], summary="Delete booking"),
)
class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):  # ok tested 
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(
            user_id=self.request.user.id
        ).select_related('room')
