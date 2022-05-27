from django.urls import include, re_path
from rest_framework import permissions, routers

from .views import MovieViewSet

router = routers.DefaultRouter()
router.register(r'', MovieViewSet)

urlpatterns = [
    re_path(r'', include(router.urls)),
]
