from django.conf import settings
from rest_framework.permissions import BasePermission


class HasServiceToken(BasePermission):
    """
    Allows the request only if the X-Service-Token header matches
    the shared token defined in settings.
    Used on Booking endpoints only.
    """
    message = "Invalid or missing X-Service-Token."

    def has_permission(self, request, view):
        token = request.META.get(settings.X_SERVICE_TOKEN_HEADER)
        return token == settings.X_SERVICE_TOKEN




    
