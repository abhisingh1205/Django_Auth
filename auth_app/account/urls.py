from django.urls import path, include
from .views import UserRegistrationView, UserLoginView, UserProfileView, UserChangePasswordView, SentPasswordResetEmailView, UserPasswordResetView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('sentresetpassword/', SentPasswordResetEmailView.as_view(), name='sentresetpassword'),
    path('resetpassword/<uid>/<token>/', UserPasswordResetView.as_view(), name='resetpassword'),
]
