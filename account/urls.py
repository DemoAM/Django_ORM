from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.views import SignUpView, EmployeeUserViewSet
from .views import login


router = DefaultRouter()
router.register("signup", SignUpView, basename="logup")
router.register("employee", EmployeeUserViewSet, basename="employee")


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/login/", login, name="login"),
]
