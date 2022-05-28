from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import status
from .models import Movie, Reservation, ReservationStatus, Seat
from .serializers import MovieSerializer, SeatLockSerializer, SeatPurchaseSerializer


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
        if self.action == 'purchase':
            return SeatPurchaseSerializer
        return super().get_serializer_class()

    @action(methods=['post'], detail=True)
    def lock(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        requested_seats = request.data["seats"].split(',')
        seats = movie.get_available_seats_for_user(request.user).filter(pk__in=requested_seats)
        if len(seats) != len(requested_seats):
            return Response("Requested seats are not available",
                            status=status.HTTP_400_BAD_REQUEST)
        reservation = Reservation.objects.create(
            movie=movie, user=request.user)
        reservation.seats.set(seats)
        return Response("Success! Seats are locked for 10 minutes", status=200)

    @action(methods=['post'], detail=True)
    def purchase(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        requested_seats = request.data["seats"].split(',')
        seats = movie.get_available_seats_for_user(request.user).filter(pk__in=requested_seats)
        if len(seats) != len(requested_seats):
            return Response("Requested seats are not available",
                            status=status.HTTP_400_BAD_REQUEST)
        reservation = Reservation.objects.create(
            movie=movie, user=request.user, status=ReservationStatus.RESERVED)
        reservation.seats.set(seats)
        return Response("Success! Seats are Reserved now!", status=200)
