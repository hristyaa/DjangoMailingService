from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView
from django.urls import path

from users.apps import UsersConfig



# from . import views


app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name='login.html')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)