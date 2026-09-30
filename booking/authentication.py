from rest_framework import exceptions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from drf_spectacular.extensions import OpenApiAuthenticationExtension


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
