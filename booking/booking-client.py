#import logging
#import requests
#from django.conf import settings
#
#logger = logging.getLogger(__name__)
#
#
#class AuthServiceError(Exception):
#    """Raised when the Auth Service returns an error or is unreachable."""
#    pass
#
#
#class AuthClient:
#    """
#    HTTP client for talking to the Auth Service.
#    Every request automatically includes the X-Service-Token header.
#    """
#
#    def __init__(self, base_url=None, token=None, timeout=5):
#        self.base_url = (base_url or settings.AUTH_SERVICE_URL).rstrip('/')
#        self.token = token or settings.X_SERVICE_TOKEN
#        self.timeout = timeout
#
#    # ─────────────────────────────────────────
#    # Internal helper
#    # ─────────────────────────────────────────
#    def _request(self, method, path, **kwargs):
#        url = f"{self.base_url}{path}"
#        headers = kwargs.pop('headers', {})
#        headers.setdefault('X-Service-Token', self.token)
#        headers.setdefault('Content-Type', 'application/json')
#
#        try:
#            response = requests.request(
#                method=method,
#                url=url,
#                headers=headers,
#                timeout=self.timeout,
#                **kwargs,
#            )
#        except requests.ConnectionError:
#            logger.error(f"[AuthClient] Cannot reach Auth Service at {url}")
#            raise AuthServiceError("Auth Service is unreachable.")
#        except requests.Timeout:
#            logger.error(f"[AuthClient] Timeout calling {url}")
#            raise AuthServiceError("Auth Service timed out.")
#
#        if not response.ok:
#            logger.warning(f"[AuthClient] {method} {url} → {response.status_code}: {response.text}")
#            raise AuthServiceError(
#                f"Auth Service error {response.status_code}: {response.text}"
#            )
#
#        # Return parsed JSON (or None for 204)
#        if response.status_code == 204 or not response.content:
#            return None
#        return response.json()
#
#    # ─────────────────────────────────────────
#    # Public methods
#    # ─────────────────────────────────────────
#    def get_user(self, user_id):
#        """Fetch a user by ID. Returns dict or raises AuthServiceError."""
#        return self._request('GET', f'/api/users/{user_id}/')
#
#    def get_current_user(self, user_jwt):
#        """
#        Fetch the user identified by a JWT.
#        Passes the JWT in the Authorization header so the Auth Service
#        knows which user is asking.
#        """
#        return self._request(
#            'GET',
#            '/api/users/me/',
#            headers={'Authorization': f'Bearer {user_jwt}'},
#        )
#
#    def verify_user_exists(self, user_id):
#        """Return True if the user exists, False if 404."""
#        try:
#            self.get_user(user_id)
#            return True
#        except AuthServiceError as e:
#            if '404' in str(e):
#                return False
#            raise