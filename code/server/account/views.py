from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import CustomUser
from .auth.serializer import UserAccountSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import bleach  # Import bleach for sanitizing input

# Sanitization function using bleach
def sanitize_input(input_data):
    """Sanitize input to remove any potential XSS attack vector."""
    return bleach.clean(input_data, tags=[], attributes={}, styles=[], strip=True)

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

class AccountView(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def get(self, request):
        # Sanitize the user data before returning
        sanitized_name = sanitize_input(request.user.name)
        serializer = UserAccountSerializer(request.user, many=False)
        # Return sanitized name with the response (if needed)
        return Response({"name": sanitized_name, **serializer.data}, status=status.HTTP_200_OK)

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

# Update any other text-based fields such as user profile description or name fields if needed.
# For example, if you have a view to update the user profile:

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]

    def put(self, request, *args, **kwargs):
        # Sanitize the name and any other text fields in the profile
        sanitized_name = sanitize_input(request.data.get("name", ""))
        sanitized_bio = sanitize_input(request.data.get("bio", ""))

        # Proceed with profile update
        user = request.user
        user.name = sanitized_name
        user.bio = sanitized_bio  # Assume bio is a field in your CustomUser model
        user.save()

        return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
