from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (UserCreateView, UserDetailView, UserListView,
                         UserLoginView, UserPasswordResetCompleteView,
                         UserPasswordResetConfirmView,
                         UserPasswordResetDoneView, UserPasswordResetView,
                         blocked_users, email_verification, unblocked_users)

# from . import views


app_name = UsersConfig.name

urlpatterns = [
    path("login/", UserLoginView.as_view(template_name='login.html'), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email_confirm"),

    path('reset_password/', UserPasswordResetView.as_view(),
         name='reset_password'),
    path('reset_password_sent/', UserPasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>', UserPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('reset_password_complete/', UserPasswordResetCompleteView.as_view(),
         name='password_reset_complete'),

    path('users/', UserListView.as_view(), name='users'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='detail_user'),
    path('users/blocked/<int:pk>/', blocked_users, name="blocked_user"),
    path('users/unblocked/<int:pk>/', unblocked_users, name="unblocked_user"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
