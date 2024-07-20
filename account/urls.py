from django.urls import path, include
from rest_framework.routers import DefaultRouter
from account.views import EmployeeUserViewSet
from .views import RegisterView, LoginView,UserProfile


router = DefaultRouter()
router.register("employee", EmployeeUserViewSet, basename="employee")
router.register("signup", RegisterView, basename="logup")
router.register('profile', UserProfile, basename="profile")


urlpatterns = [
    path("api/", include(router.urls)),
    path("api/login/", LoginView.as_view()),
]
