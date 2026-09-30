from django.urls import path
from .views import BookingListCreateView, BookingDetailView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('bookings/',          BookingListCreateView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetailView.as_view(),     name='booking-detail'),
    path('token/refresh/', TokenRefreshView.as_view()),
]
