from rest_framework.viewsets import ModelViewSet
from account.models import User
from account.serializers import LogUpSerializer, EmployeeUserSerializer, UserProfileSerializer
from .models import Role
from rest_framework import status
from rest_framework.response import Response
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken , AccessToken
from rest_framework.permissions import IsAuthenticated


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = AccessToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(access_token),
    }

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            user = authenticate(request, email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response(
                    {"token": token, "message": "Login Successful"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"detail": "Invalid Credentials"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = LogUpSerializer
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response(
            {
                "token": token,
                "message": "Registration Success"
            },
            status=status.HTTP_200_OK,
        )


class EmployeeUserViewSet(ModelViewSet):
    queryset = User.objects.filter(role=Role.Roles.EMPLOYEE)
    serializer_class = EmployeeUserSerializer


class UserProfile(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = IsAuthenticated
    http_method_names = ['get']

    def get_queryset(self):
        return User.objects.filter(email=self.request.user.email)



