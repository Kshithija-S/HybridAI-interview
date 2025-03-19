import jwt
import datetime
from django.conf import settings

# Secret key for signing JWT tokens
SECRET_KEY = settings.SECRET_KEY  # Use Django's SECRET_KEY

def create_jwt_token(user):
    """
    Generate JWT token for a given user.
    """
    payload = {
        'user_id': user.id,
        'username': user.username,
        'exp': datetime.datetime.now() + datetime.timedelta(days=1),  # Token expires in 1 day
        'iat': datetime.datetime.now()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_jwt_token(token):
    """
    Verify and decode a JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload  # Returns decoded payload (user_id, username, etc.)
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
