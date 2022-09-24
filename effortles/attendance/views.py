import calendar
from datetime import datetime, timedelta

from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.views.generic.dates import MonthArchiveView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Attendance, Swipes


User = get_user_model()


def get_swipes(current_month_attendance_queryset):
    """
        utility function to fetch the swipes of every date
        and return a list of dictionary containing 
        - date
        - total working hour
        - status (decided on total working hours)

        parameter:        
        - current_month_attendance_queryset: (variable holding quesry set of 
        current month attendance)
    """

    attendance_with_status = []
    
    for attendance in current_month_attendance_queryset:
        print(attendance)
        swipes_on_the_day = Swipes.objects.filter(attendance_id = attendance.id)
        total_working_hour = timedelta(hours=0, minutes=0, seconds=0)
        status = None
        swipe_pair_count =  len(swipes_on_the_day)//2
      
        swipe_pair_iter = 0
        while swipe_pair_iter < swipe_pair_count:
           
            swipe_in_timedelta = timedelta(
                                    hours = swipes_on_the_day[(swipe_pair_iter*2)].time_of_swipe.hour,
                                    minutes = swipes_on_the_day[(swipe_pair_iter*2)].time_of_swipe.minute,
                                    seconds = swipes_on_the_day[(swipe_pair_iter*2)].time_of_swipe.second
                                    )
            swipe_out_timedelta = timedelta(
                                    hours = swipes_on_the_day[(swipe_pair_iter*2)+1].time_of_swipe.hour,
                                    minutes = swipes_on_the_day[(swipe_pair_iter*2)+1].time_of_swipe.minute,
                                    seconds = swipes_on_the_day[(swipe_pair_iter*2)+1].time_of_swipe.second
                                    )

            total_working_hour+=(swipe_out_timedelta-swipe_in_timedelta)
            swipe_pair_iter+=1

        if( total_working_hour >= timedelta(hours=8)):
            status = "present"
        elif( total_working_hour<timedelta(hours=8) and total_working_hour>=timedelta(hours=4) ):
            status = "half_day_leave"
        else:
            status = "loss_of_pay_leave"
        

        attendance_with_status.append({
            "date": attendance.date,
            "working_hours": total_working_hour,
            "status": status, 
        })

    return attendance_with_status


class SwipeMarkView(LoginRequiredMixin, CreateView):
    
    def get(self, request):
        """
        overriding the get() method, here 
        - retriving attendance of current month form the database
        - calling the utility function to give date with status
        - making the month calender with the dates and status on it
        - sending the calendar in the context object
        """

        attendance = Attendance.objects.filter(user=request.user.id, date__date=datetime.now().date())

        if not attendance.exists():
           
            todays_attendance = Attendance(user_id=request.user.id, swipe_status="swiped_in")
            todays_attendance.save()
            current_swipe = Swipes(attendance_id=Attendance(todays_attendance.id), swipe_status="swiped_in")
            current_swipe.save()
            
            return redirect('/authentication/dashboard')
        
        else:
            current_swipe = Swipes.objects.filter(attendance_id=attendance.first().id).last()

            if current_swipe == None:
                current_swipe = Swipes(attendance_id=Attendance(attendance.first().id), swipe_status="swiped_in")
                current_swipe.save()

            elif current_swipe.swipe_status != "swiped_in":
                current_swipe = Swipes(attendance_id=Attendance(attendance.first().id), swipe_status="swiped_in")
                current_swipe.save()
            
            else:    
                current_swipe = Swipes(attendance_id=Attendance(attendance.first().id), swipe_status="swiped_out")
                current_swipe.save()

            return redirect('/authentication/dashboard')
        

class ShowCalender(LoginRequiredMixin, MonthArchiveView):
    
    def get(self, request):
        """
            this function return the current month calendar

            - gets current month and current year
            - gets current month calendar
            - add attendance status on every date
        """
        
        current_month =  datetime.now().month
        current_year = datetime.now().year
        current_month_calendar = calendar.monthcalendar(current_year,current_month)
        starting_day_of_month = calendar.monthrange(current_year,current_month)[0]

        current_attendance = Attendance.objects.filter( user=request.user.id, date__month=current_month, date__year=current_year)
        current_attendance_with_status = get_swipes(current_attendance)
        
        date_with_status = [0]*(len(current_month_calendar)*7)

        for day in current_attendance_with_status:          
            date_with_status[ int(str(day["date"].date())[-2:]) ] = day["status"]

        current_month_calendar_with_status = []

        day_count = 1
        date_with_status_count = 1
        for week in current_month_calendar:
            week_temp = []
            for day in week:
                if day_count>starting_day_of_month:
                    if date_with_status[date_with_status_count] == 0:
                        week_temp.append({"date":day, "status":"N/A"})
                    else:
                        week_temp.append({"date":day, "status":date_with_status[date_with_status_count]})
                    
                    date_with_status_count+=1
                else:
                     week_temp.append({"date":day, "status":"N/A"})
                     
                day_count+=1
            current_month_calendar_with_status.append(week_temp)
        
        calender_context = {
            "current_month_calendar_with_status": current_month_calendar_with_status
        }

        return render(request, "attendance/calendar.html", calender_context)
      