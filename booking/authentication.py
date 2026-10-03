from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension

class SimpleUser:
    """
    A stateless user object — no DB, no model.
    Created from the JWT payload on every request.
    """
    def __init__(self, user_id, claims=None):
        self.id = user_id
        self.pk = user_id
        self.is_active = True
        self.is_authenticated = True
        self.is_anonymous = False
        self.claims = claims or {}

        # Optional convenience attributes
        self.username = self.claims.get('username', '')
        self.email = self.claims.get('email', '')

    def __str__(self):
        return f"SimpleUser(id={self.id}, username={self.username})"

    def __repr__(self):
        return self.__str__()

    
class StatelessJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise exceptions.AuthenticationFailed('Token has no user_id claim')

        user = self.user_model(**{api_settings.USER_ID_FIELD: user_id})
        user.is_active = True
        for claim in ('username', 'email'):
            if claim in validated_token:
                setattr(user, claim, validated_token[claim])
        return user


class StatelessJWTAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = 'booking.authentication.StatelessJWTAuthentication'
    name = 'BearerAuth'

    def get_security_definition(self, auto_schema):
        return {'type': 'http', 'scheme': 'bearer', 'bearerFormat': 'JWT'}
