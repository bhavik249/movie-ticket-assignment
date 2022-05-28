from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Movie, Reservation, Seat
from .serializers import MovieSerializer, SeatLockSerializer


class LockAndPurchaseAunticated(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'lock' and not request.user.is_authenticated:
            return False
        return True


class MovieViewSet(GenericViewSet, mixins.ListModelMixin):
    permission_classes = (LockAndPurchaseAunticated,)
    http_method_names = ['get', 'post']
    lookup_field = 'id'
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer

    def get_serializer_class(self):
        if self.action == 'lock':
            return SeatLockSerializer

        return super().get_serializer_class()

    @action(methods=['post'], detail=True)
    def lock(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        seats = []
        for seat in request.data["seats"].split(','):
            seats.append(get_object_or_404(Seat, pk=seat))
        serializer.is_valid(raise_exception=True)
        reservation = Reservation.objects.create(
            movie=movie, user=request.user)
        reservation.seats.set(seats)
        return Response(status=200)
