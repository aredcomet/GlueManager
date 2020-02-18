from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    LoginView,
    LogoutView,
    LogoutAllView,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = router.urls

urlpatterns += [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/logout-all/', LogoutAllView.as_view(), name='logout-all'),
]