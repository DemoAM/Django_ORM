from rest_framework.viewsets import ModelViewSet
from account.models import User
from account.serializers import SignUpSerializer, EmployeeUserSerializer
from .models import Role
from rest_framework import status
from rest_framework.response import Response
from .serializers import LoginSerializer
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view


@api_view(["post"])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        email = serializer.data.get("email")
        password = serializer.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            return Response("Login Successful", status=status.HTTP_200_OK)
        return Response(
            {"detail": "Credentials Not Found."}, status=status.HTTP_404_NOT_FOUND
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    # http_method_names = ["post"]
    permission_classes = []


class EmployeeUserViewSet(ModelViewSet):
    queryset = User.objects.filter(role=Role.Roles.EMPLOYEE)
    serializer_class = EmployeeUserSerializer
