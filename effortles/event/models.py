from django.db import models
from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()


class Event(models.Model):
    
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    event_name = models.CharField(max_length=256)
    date = models.DateField(null=False)
    amount = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    participant = models.ManyToManyField(
        User, related_name='participant_table', through='Participant')


class Participant(models.Model):
    TRANSACTION_STATUS = [
        ("Not Confirmed", "not_confirmed"),
        ("Confirmed", "confirmed"),
    ]

    user = models.ForeignKey(
        User, related_name='user_participating_in_the_event', on_delete=models.DO_NOTHING)
    event = models.ForeignKey(
        Event, related_name='event_to_be_participate_in', on_delete=models.DO_NOTHING)
    transaction_status = models.CharField(
        choices=TRANSACTION_STATUS, max_length=16, default="not_confirmed", null=False)
    transaction_key = models.CharField(max_length=256, null=False)
