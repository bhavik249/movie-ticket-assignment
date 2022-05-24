# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Movie, Reservation, Seat


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'price',
                    'start', 'end']
    search_fields = ['name', 'description', 'price']
    list_filter = ['start', 'end']
    actions = ['delete_selected']


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['row', 'seat_no']
    actions = ['delete_selected']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['movie', 'status', 'user']
    list_filter = ['movie', 'user', 'seats', 'status']
    actions = ['delete_selected']
