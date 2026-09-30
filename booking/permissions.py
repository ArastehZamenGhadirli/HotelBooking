from django.conf import settings
from rest_framework.permissions import BasePermission
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
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




User = get_user_model()


class HasValidJWT(BasePermission):
    message = "Invalid or missing JWT."

    def has_permission(self, request, view):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')

        if not auth_header:
            return False

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return False

        token = parts[1]

        signing_key = settings.SIMPLE_JWT.get('SIGNING_KEY', settings.SECRET_KEY)

        try:
            payload = jwt.decode(
                token,
                signing_key,
                algorithms=[settings.SIMPLE_JWT.get('ALGORITHM', 'HS256')],
            )
        except jwt.ExpiredSignatureError:
            self.message = "Token has expired."
            return False
        except jwt.InvalidTokenError as e:
            self.message = f"Token is invalid: {e}"
            return False

        user_id = payload.get('user_id')
        if not user_id:
            self.message = "Token has no user_id."
            return False

        request.user = SimpleUser(user_id=user_id, payload=payload)
        return True
    