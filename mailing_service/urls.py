from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from mailing_service.apps import MailingServiceConfig
from mailing_service.views import *

# from . import views


app_name = MailingServiceConfig.name

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("clients/", MailingRecipientListView.as_view(), name="clients"),
    path("clients/create/", MailingRecipientCreateView.as_view(), name="create_client"),
    path("clients/<int:pk>/", MailingRecipientDetailView.as_view(), name="detail_client"),
    path("clients/update/<int:pk>/", MailingRecipientUpdateView.as_view(), name="update_client"),
    path("clients/delete/<int:pk>/", MailingRecipientDeleteView.as_view(), name="delete_client"),
    path("messages/", MailingMessageListView.as_view(), name="messages"),
    path("messages/create/", MailingMessageCreateView.as_view(), name="create_message"),
    path("messages/<int:pk>/", MailingMessageDetailView.as_view(), name="detail_message"),
    path("messages/update/<int:pk>/", MailingMessageUpdateView.as_view(), name="update_message"),
    path("messages/delete/<int:pk>/", MailingMessageDeleteView.as_view(), name="delete_message"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
