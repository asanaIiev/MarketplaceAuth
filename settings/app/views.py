from rest_framework.request import Request
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)

        return Response({
            'detail': 'Successfully registered',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')
        refresh = RefreshToken.for_user(user)

        return Response({
            'detail': 'Successfully logged in',
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        })

class LogoutView(APIView):
    def post(self, request):
        try:
            refresh = request.data.get('refresh')
            if not refresh:
                return Response({'detail': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

            token = RefreshToken(refresh)
            token.blacklist()
            return Response({
                'detail': 'Successfully logged out'
            }, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({
                'detail': 'Invalid token'
            }, status=status.HTTP_400_BAD_REQUEST)