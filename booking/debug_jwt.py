import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookingmangment.settings')
django.setup()

from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

print("SIGNING_KEY:", repr(settings.SIMPLE_JWT.get('SIGNING_KEY')))

token = input("Paste token: ").strip()
try:
    t = AccessToken(token)
    print("✅ VALID. Payload:", dict(t))
except TokenError as e:
    print("❌ INVALID:", e)


