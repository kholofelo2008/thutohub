from django.urls import path
from .views import (RegisterView, CustomLoginView, CustomLogoutView,
ProfileView,ProfileUpdateView)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
]