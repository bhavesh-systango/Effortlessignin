from django.http import HttpResponse
from django.shortcuts import render



from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from attendance.models import Attendance, Swipes
from django.db.models import FilteredRelation, Q
from django.db import connection

User = get_user_model()


def attendance_round_off(requset):
    previous_date = datetime.today() # TODO: remove this line
    print(previous_date.date())
    
    all_user = User.objects.filter( is_superuser = 0 ).values('pk')
    all_previous_day_attendance = Attendance.objects.filter(date__date=previous_date).values('user')

    all_user_id_set = set()

    for all_user_itr in all_user:
        all_user_id_set.add(all_user_itr['pk'])

    for all_previous_day_attendance_itr in all_previous_day_attendance:
        all_user_id_set.discard(all_previous_day_attendance_itr['user'])

    all_user_id_set_absent_set = all_user_id_set

    attendance_entries = []
    
    for id_iter in all_user_id_set_absent_set:
        attendance_entries.append(
            Attendance(user=User(id_iter), attendance_status="loss_of_pay_leave", swipe_status="absent")
        )
        

    Attendance.objects.bulk_create(
        attendance_entries
    )


        