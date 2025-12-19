from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from bio import views

# These URLs will not have a language prefix
urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),  # Added for set_language view
]

# These URLs will have a language prefix (e.g., /en/explore/)
urlpatterns += i18n_patterns(
    path("", views.home, name="home"),
    path("explore/", views.explore, name="explore"),
    path("trending/", views.trending, name="trending"),
    path("upload/", views.upload_file, name="upload_file"),
    path("bio/", include("bio.urls")),
)

# Media files serving for development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
