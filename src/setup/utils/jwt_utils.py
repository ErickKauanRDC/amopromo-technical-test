from datetime import datetime, timedelta
import jwt
from django.conf import settings

class JWTUtils:
    @staticmethod
    def encode(payload: dict, secret: str = None, algorithm: str = 'HS256'):
        """
        Encodes the payload into a JWT token.
        """
        secret = settings.SECRET_KEY
        expiration = datetime.now(datetime.timezone.utc) + timedelta(hours=1) 
        payload.update({"exp": expiration})
        return jwt.encode(payload, secret, algorithm=algorithm)

    @staticmethod
    def decode(token: str, secret: str = None, algorithms: str = 'HS256'):
        """
        Decodes the JWT token into a payload.
        """
        secret = settings.SECRET_KEY
        try:
            return jwt.decode(token, secret, algorithms=[algorithms])
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError:
            raise ValueError("Invalid token")

