from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Attendance(models.Model):
    ATTENDANCE_STATUS = [
        ("present","Present"),
        ("loss_of_pay_leave","Loss Of Pay Leave"),
        ("paid_leave","Paid Leave"),
        ("half_day_leave","Half Day Leave"),
    ]

    SWIPE_STATUS = [
        ("swiped_in","Swiped In"),
        ("swiped_out","Swiped Out"),
        ("absent", "Absent")
    ]

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    attendance_status = models.CharField(max_length=20, choices=ATTENDANCE_STATUS)
    swipe_status = models.CharField(max_length=10, choices=SWIPE_STATUS)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} ___ {self.user} ___ {self.date}"


class Swipes(models.Model):
    SWIPE_STATUS = [
        ("swiped_in","Swiped In"),
        ("swiped_out","Swiped Out")
    ]

    attendance_id = models.ForeignKey(Attendance, on_delete=models.DO_NOTHING)
    time_of_swipe = models.TimeField(auto_now_add=True)
    swipe_status = models.CharField(max_length=10, choices=SWIPE_STATUS)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
