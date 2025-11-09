from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from mailing_service.apps import MailingServiceConfig
from mailing_service.views import HomePageView, MailingRecipientListView, MailingRecipientCreateView

# from . import views


app_name = MailingServiceConfig.name

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("clients/", MailingRecipientListView.as_view(), name="clients"),
    path("clients/create/", MailingRecipientCreateView.as_view(), name="create_client"),
    # path("posts/<int:pk>/", BlogPostDetailView.as_view(), name="post_detail"),
    # path("posts/create/", BlogPostCreateView.as_view(), name="post_create"),
    # path("posts/update/<int:pk>/", BlogPostUpdateView.as_view(), name="post_update"),
    # path("posts/delete/<int:pk>/", BlogPostDeleteView.as_view(), name="post_delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
