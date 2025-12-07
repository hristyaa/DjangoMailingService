from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, UserPasswordResetView, UserPasswordResetDoneView, UserPasswordResetConfirmView, UserPasswordResetCompleteView

# from . import views


app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name='login.html'), name="login"),
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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
