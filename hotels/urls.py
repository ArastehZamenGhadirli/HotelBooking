from django.urls import path
from .views import (
    HotelListCreateView, HotelDetailView,
    RoomListCreateView, RoomDetailView,HotelRoomsListView
)

urlpatterns = [
    path('hotels/',          HotelListCreateView.as_view(),  name='hotel-list'),
    path('hotels/<int:pk>/', HotelDetailView.as_view(),      name='hotel-detail'),
    path('rooms/',           RoomListCreateView.as_view(),   name='room-list'),
    path('rooms/<int:pk>/',  RoomDetailView.as_view(),       name='room-detail'),
     path('hotels/<int:pk>/rooms/',     HotelRoomsListView.as_view(),  name='hotel-rooms'), 
]