from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.UserSignUpView.as_view(), name='user_signup'),
    path('login', views.UserLoginView.as_view(), name='user_login'),
    # path('logout', views.UserLogoutView.as_view(), name='user_logout'),
    path('token/refresh', views.RefreshTokenView.as_view(), name='refresh_token'),
]
