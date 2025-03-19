from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserCreateSerializer, UserResponseSerializer, LoginSerializer
from .sqlalchemy_models import SessionLocal, User, hash_password, verify_password
from sqlalchemy.exc import IntegrityError
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime

def get_tokens_for_user(user_id, username):
    # Generate JWT tokens for user

    token = AccessToken()
    token['user_id'] = user_id
    token['username'] = username

    return {
        'jwt': str(token),
    }

@method_decorator(csrf_exempt, name='dispatch')
class UserCreateAPIView(APIView):
   
    def post(self, request, format=None):
        serializer = UserCreateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        full_name = serializer.validated_data.get('full_name', '')
        
        db = SessionLocal()
        
        try:
            if db.query(User).filter(User.username == username).first():
                db.close()
                return Response(
                    {"error": "Username already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if db.query(User).filter(User.email == email).first():
                db.close()
                return Response(
                    {"error": "Email already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            hashed_password = hash_password(password)
            new_user = User(
                username=username,
                email=email,
                full_name=full_name,
                hashed_password=hashed_password
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            response_data = {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'full_name': new_user.full_name,
            }
            
            tokens = get_tokens_for_user(new_user.id, new_user.username)
            
            response_serializer = UserResponseSerializer(response_data)
            return Response({
                'user': response_serializer.data,
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
            
        except IntegrityError as e:
            db.rollback()
            return Response(
                {"error": f"Database integrity error: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            db.rollback()
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            db.close()
