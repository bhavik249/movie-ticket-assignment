from django.db import models

# http://learnmongodbthehardway.com/schema/theater/


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


class Theater(models.Model):
    name = models.CharField(max_length=255)


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
