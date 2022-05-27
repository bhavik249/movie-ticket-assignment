from rest_framework import serializers

from .models import Movie, Seat


class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat
        fields = ('id', 'row', 'seat_no')


class MovieSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(Seat.objects.all(), many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('id', 'name', 'description', 'start', 'end', 'price', 'seats', 'reservations')
