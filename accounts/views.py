from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from companies.models import Company
from .models import User
from .serializers import LoginSerializer, UserSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access':  str(refresh.access_token),
    }


class LoginView(APIView):
    """
    POST /api/auth/login/
    Body: { "company_code": "VISR", "user_code": "USR001", "password": "****" }
    Returns JWT tokens + user info.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        company_code = serializer.validated_data['company_code'].upper().strip()
        user_code    = serializer.validated_data['user_code'].upper().strip()
        password     = serializer.validated_data['password']

        # Validate company
        try:
            company = Company.objects.get(code=company_code, is_active=True)
        except Company.DoesNotExist:
            return Response(
                {'detail': 'Invalid company code.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        # Validate user
        try:
            user = User.objects.get(company=company, user_code=user_code, is_active=True)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Invalid user code or password.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.check_password(password):
            return Response(
                {'detail': 'Invalid user code or password.'},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        tokens = get_tokens_for_user(user)

        return Response(
            {
                'tokens': tokens,
                'user':   UserSerializer(user).data,
            },
            status=status.HTTP_200_OK,
        )


class MeView(APIView):
    """
    GET /api/auth/me/
    Returns current logged-in user's profile. Requires Authorization header.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)
