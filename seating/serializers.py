from rest_framework import serializers
from django.db.models import Q
from .models import Movie, Reservation, Seat, Theater, ReservationStatus
from datetime import timedelta
from django.utils import timezone


class SeatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seat
        fields = ('id', 'row', 'seat_no')


class MovieSerializer(serializers.ModelSerializer):
    available_seats = serializers.SerializerMethodField()

    def get_available_seats(self, obj):
        return SeatSerializer(instance=obj.get_available_seats(), many=True).data

    class Meta:
        model = Movie
        fields = ('id', 'name', 'description', 'start',
                  'end', 'price', 'theater', 'available_seats')


class SeatLockSerializer(serializers.ModelSerializer):
    seats = serializers.CharField()

    class Meta:
        model = Movie
        fields = ('seats',)


class SeatPurchaseSerializer(SeatLockSerializer):
    payment = serializers.CharField()

    class Meta:
        model = Movie
        fields = ('seats', 'payment')
