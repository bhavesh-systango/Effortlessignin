import kronos
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from attendance.models import Attendance, Swipes


User = get_user_model()


# @kronos.register('13 * * * mon-fri')
# @kronos.register('* * * * mon-fri')
@kronos.register('0 0 * * mon-fri')
class Command(BaseCommand):    
    help = "this command will round of attendance and mark a\
            attendance status, according to the swipe times."

    def handle(self, *args, **options):
        """
            function will calculate the working hour and mark the attendance

            - get the previous day date 
            - take out all the object of user
            - take all the object of previous day attendance
            - check which user have started the attendance which have not
            - the user who have started the attendance taken out
            - working hours is calculated on the basis of the Swipe history
        """
        print("attendance round off worked")
        
        # previous_date = datetime.today() - timedelta(days=1) 
        previous_date = datetime.today()
        
        all_previous_day_attendance = Attendance.objects.filter(date__date=previous_date)
        print(all_previous_day_attendance)

        # for attendance in all_previous_day_attendance:

        #     swipes_on_the_day = Swipes.objects.filter(attendance_id = attendance.id)
        #     total_working_hour = timedelta(hours=0, minutes=0, seconds=0)
        #     swipe_pair_count =  len(swipes_on_the_day)//2

        #     swipe_pair_iter = 0
        #     while swipe_pair_iter < swipe_pair_count:
           
        #         swipe_in_timedelta = timedelta(
        #                             hours = swipes_on_the_day[(swipe_pair_iter*2)].time_of_swipe.hour,
        #                             minutes = swipes_on_the_day[(swipe_pair_iter*2)].time_of_swipe.minute,
        #                             seconds = swipes_on_the_day[(swipe_pair_iter*2)].time_of_swipe.second
        #                             )
        #         swipe_out_timedelta = timedelta(
        #                             hours = swipes_on_the_day[(swipe_pair_iter*2)+1].time_of_swipe.hour,
        #                             minutes = swipes_on_the_day[(swipe_pair_iter*2)+1].time_of_swipe.minute,
        #                             seconds = swipes_on_the_day[(swipe_pair_iter*2)+1].time_of_swipe.second
        #                             )

        #         total_working_hour+=(swipe_out_timedelta-swipe_in_timedelta)
        #         swipe_pair_iter+=1

        #     if( total_working_hour >= timedelta(hours=8)):
        #         attendance.attendance_status = "present"
        #     elif( total_working_hour>=timedelta(hours=4) and total_working_hour<timedelta(hours=8)):
        #         attendance.attendance_status = "half_day_leave"
        #     else:
        #         attendance.attendance_status = "loss_of_pay_leave"

        #     attendance.save()
        
