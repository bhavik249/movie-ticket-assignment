from attr import field
from rest_framework import serializers

from .models import Movie, Seat, Theater


class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat
        fields = ('id', 'row', 'seat_no')


class TheaterSerializer(serializers.ModelSerializer):
    seats = SeatSerializer(Seat.objects.all(), many=True)

    class Meta:
        model = Theater
        fields = ('id', 'name', 'seats')


class MovieSerializer(serializers.ModelSerializer):
    theater = TheaterSerializer()

    class Meta:
        model = Movie
        fields = ('id', 'name', 'description', 'start',
                  'end', 'price', 'theater', 'reservations')
