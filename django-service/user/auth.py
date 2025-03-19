from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .utils import verify_jwt_token
from .sqlalchemy_models import SessionLocal, User

class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return None  # No authentication provided
        
        token = auth_header.split(' ')[1]  # Extract token
        payload = verify_jwt_token(token)

        if not payload:
            raise AuthenticationFailed("Invalid or expired token")

        # Retrieve user from database
        db = SessionLocal()
        user = db.query(User).filter(User.id == payload['user_id']).first()
        db.close()

        if not user:
            raise AuthenticationFailed("User not found")

        return (user, None)
