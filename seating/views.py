from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .models import Movie
from .serializers import MovieSerializer


class MovieViewSet(GenericViewSet, mixins.ListModelMixin):
    permission_classes = ()
    http_method_names = ['get', 'post']
    lookup_field = 'id'
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
