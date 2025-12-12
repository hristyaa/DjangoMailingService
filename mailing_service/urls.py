from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.decorators.cache import cache_page

from mailing_service.apps import MailingServiceConfig
from mailing_service.views import (
    HomePageView,
    MailingCreateView,
    MailingDeleteView,
    MailingDetailView,
    MailingListView,
    MailingMessageCreateView,
    MailingMessageDeleteView,
    MailingMessageDetailView,
    MailingMessageListView,
    MailingMessageUpdateView,
    MailingRecipientCreateView,
    MailingRecipientDeleteView,
    MailingRecipientDetailView,
    MailingRecipientListView,
    MailingRecipientUpdateView,
    MailingSendView,
    MailingUpdateView,
    disable_mailing,
    mailing_report,
)

# from . import views


app_name = MailingServiceConfig.name

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path(
        "clients/", cache_page(60)(MailingRecipientListView.as_view()), name="clients"
    ),
    path("clients/create/", MailingRecipientCreateView.as_view(), name="create_client"),
    path(
        "clients/<int:pk>/",
        cache_page(60)(MailingRecipientDetailView.as_view()),
        name="detail_client",
    ),
    path(
        "clients/update/<int:pk>/",
        MailingRecipientUpdateView.as_view(),
        name="update_client",
    ),
    path(
        "clients/delete/<int:pk>/",
        MailingRecipientDeleteView.as_view(),
        name="delete_client",
    ),
    path(
        "messages/", cache_page(60)(MailingMessageListView.as_view()), name="messages"
    ),
    path("messages/create/", MailingMessageCreateView.as_view(), name="create_message"),
    path(
        "messages/<int:pk>/",
        cache_page(60)(MailingMessageDetailView.as_view()),
        name="detail_message",
    ),
    path(
        "messages/update/<int:pk>/",
        MailingMessageUpdateView.as_view(),
        name="update_message",
    ),
    path(
        "messages/delete/<int:pk>/",
        MailingMessageDeleteView.as_view(),
        name="delete_message",
    ),
    path("mailings/", MailingListView.as_view(), name="mailings"),
    path("mailings/create/", MailingCreateView.as_view(), name="create_mailing"),
    path("mailings/<int:pk>/", MailingDetailView.as_view(), name="detail_mailing"),
    path(
        "mailings/update/<int:pk>/", MailingUpdateView.as_view(), name="update_mailing"
    ),
    path(
        "mailings/delete/<int:pk>/", MailingDeleteView.as_view(), name="delete_mailing"
    ),
    path("mailings/send/<int:pk>/", MailingSendView.as_view(), name="send_mailing"),
    path("attempts/", mailing_report, name="attempts"),
    path("mailings/disable/<int:pk>/", disable_mailing, name="disable_mailing"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
