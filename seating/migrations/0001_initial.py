# Generated by Django 3.2.4 on 2022-05-24 17:53

import datetime
from django.utils import timezone

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

seat_rows = "ABCDEFGHIJKL"
total_seats_in_row = 15

movies = [
    {
        "name": "RRR",
        "description": "Action movie",
        "start": timezone.now() + datetime.timedelta(days=1),
        "end": timezone.now() + datetime.timedelta(days=1, hours=3),
        "price": 300
    },
    {
        "name": "KGF-2",
        "description": "Action movie",
        "start": timezone.now() + datetime.timedelta(days=2),
        "end": timezone.now() + datetime.timedelta(days=2, hours=3),
        "price": 300
    }
]


def forwards_func(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Movie = apps.get_model("seating", "Movie")
    for movie in movies:
        Movie.objects.using(db_alias).create(**movie)
    Seat = apps.get_model("seating", "Seat")
    for row in seat_rows:
        for seat in range(1, total_seats_in_row):
            Seat.objects.using(db_alias).create(row=row, seat_no=seat)


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Seat',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(
                    auto_now_add=True, db_index=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('row', models.CharField(max_length=1)),
                ('seat_no', models.CharField(max_length=2)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(
                    auto_now_add=True, db_index=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, null=True)),
                ('is_active', models.BooleanField(db_index=True, default=True)),
                ('status', models.CharField(choices=[('LOCKED', 'Locked'), ('RESERVED', 'Reserved'), (
                    'CANCELED', 'Canceled')], default='LOCKED', max_length=10)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                 related_name='reservations', to='seating.movie')),
                ('seats', models.ManyToManyField(
                    related_name='reservations', to='seating.Seat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT,
                 related_name='reservations', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RunPython(forwards_func, migrations.RunPython.noop),
    ]
