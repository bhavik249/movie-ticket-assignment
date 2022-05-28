from datetime import timedelta

from django.db import models
from django.db.models import Q
from django.utils import timezone
from yaml import load


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, null=True, blank=True)
    updated_at = models.DateTimeField(
        auto_now=True, db_index=True, null=True, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True


class Movie(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start = models.DateTimeField()
    end = models.DateTimeField()
    price = models.FloatField()
    theater = models.ForeignKey(
        'seating.Theater', on_delete=models.PROTECT, related_name='movies')

    def __str__(self) -> str:
        return self.name

    def get_available_seats_for_user(self, user=None):
        time_threshold = timezone.now() - timedelta(minutes=10)
        # Locking will work only for 10 minutes and available after 10 minutes if not purchased
        locked_seats = Reservation.objects.filter(
            Q(status=ReservationStatus.LOCKED) & Q(updated_at__gt=time_threshold))
        if user:
            locked_seats = locked_seats.filter(~Q(user=user))
        locked_seats = locked_seats.values_list('id', flat=True)
        return Seat.objects.filter(~models.Q(reservations__status=ReservationStatus.RESERVED)).exclude(reservations__id__in=locked_seats)


class Theater(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Seat(BaseModel):
    theater = models.ForeignKey(
        'seating.Theater', on_delete=models.CASCADE, related_name='seats')
    row = models.CharField(max_length=1)
    seat_no = models.CharField(max_length=2)

    def __str__(self) -> str:
        return f"{self.row}-{self.seat_no}"


class ReservationStatus(models.TextChoices):
    LOCKED = 'LOCKED'
    RESERVED = 'RESERVED'
    CANCELED = 'CANCELED'


class Reservation(BaseModel):
    movie = models.ForeignKey(
        "seating.Movie", on_delete=models.PROTECT, related_name="reservations")
    seats = models.ManyToManyField(
        "seating.Seat", related_name="reservations")
    status = models.CharField(
        max_length=10, choices=ReservationStatus.choices, default=ReservationStatus.LOCKED)
    user = models.ForeignKey(
        "user.CustomUser", on_delete=models.PROTECT, related_name="reservations")

    def __str__(self) -> str:
        return f"{self.movie} {self.user} {self.status}"
