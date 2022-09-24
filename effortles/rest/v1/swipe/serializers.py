from django.contrib.auth import get_user_model
from rest_framework import serializers
from attendance.models import Attendance, Swipes

User = get_user_model()

class AttendanceSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        many=False, 
        read_only=False,
        queryset=User.objects.all(),
    )

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'user',
            'date',
            'attendance_status',
            'swipe_status',
            'updated_at',
        ]


class SwipeSerializer(serializers.ModelSerializer):

    attendance_id = serializers.PrimaryKeyRelatedField(
        many=False, 
        read_only=False,
        queryset=Attendance.objects.all(),
    )

    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Swipes
        fields = [
            'attendance_id',
            'time_of_swipe',
            'swipe_status',
            'created_at',
            'updated_at',
        ]

