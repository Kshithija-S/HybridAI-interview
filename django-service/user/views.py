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
from .auth import JWTAuthentication
from .utils import create_jwt_token

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
            
            token = create_jwt_token(new_user)
            
            response_serializer = UserResponseSerializer(response_data)
            return Response({
                'user': response_serializer.data,
                'tokens': token
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

@method_decorator(csrf_exempt, name='dispatch')
class UserLoginAPIView(APIView):
    
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated data
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        
        # Create SQLAlchemy session
        db = SessionLocal()
        
        try:
            # Find user by username or email
            query = db.query(User)
            if username:
                user = query.filter(User.username == username).first()
            else:
                user = query.filter(User.email == email).first()
            
            # Check if user exists and password is correct
            if not user or not verify_password(password, user.hashed_password):
                return Response(
                    {"error": "Invalid credentials"},
                    status=status.HTTP_401_UNAUTHORIZED
                )
            
            # Update last login
            user.last_login = datetime.now()
            db.commit()
            
            # Generate tokens
            tokens = create_jwt_token(user)
            
            response_serializer = UserResponseSerializer(user)
            return Response({
                'user': response_serializer.data,
                'tokens': tokens
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            db.close()

class UserActivityAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        db = SessionLocal()
        try:
            print(request)
            user = db.query(User).filter(User.id == request.user.id).first()
            print(user)
            if not user:
                return Response(
                    {"error": "User not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
            response_serializer = UserResponseSerializer(user)
            return Response({
                'user': response_serializer.data,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            db.close()