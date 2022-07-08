from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views
from django.contrib import admin
from django.urls import include, path

from api.views import PostViewSet, GroupViewSet, CommentViewSet, UserViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comments'
                )
router.register(r'users', UserViewSet)


urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
