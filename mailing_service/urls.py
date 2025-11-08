from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from mailing_service.apps import MailingServiceConfig


# from . import views


app_name = MailingServiceConfig.name

urlpatterns = [
    # path("posts/", BlogPostListView.as_view(), name="posts_list"),
    # path("posts/<int:pk>/", BlogPostDetailView.as_view(), name="post_detail"),
    # path("posts/create/", BlogPostCreateView.as_view(), name="post_create"),
    # path("posts/update/<int:pk>/", BlogPostUpdateView.as_view(), name="post_update"),
    # path("posts/delete/<int:pk>/", BlogPostDeleteView.as_view(), name="post_delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
