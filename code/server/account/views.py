from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from .auth.serializer import UserAccountSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import CustomUser

from django.contrib.auth import authenticate

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        # Authenticate user
        user = authenticate(email=request.data["email"], password=request.data["password"])
        
        if user is None:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not user.is_active:
            return Response({'message': 'User is not active.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # If user is authenticated and active, proceed with token generation
        return super().post(request, *args, **kwargs)

        # Generate JWT token
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({"access": access_token, "refresh": str(refresh)}, status=status.HTTP_200_OK)

	
class AccountView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
        serializer = UserAccountSerializer(request.user, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                return Response({"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.block()  # Block the refresh token so it can't be used again
            
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"message": "Invalid token or error in processing"}, status=status.HTTP_400_BAD_REQUEST)



