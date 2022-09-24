from datetime import datetime 
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from attendance.models import Attendance, Swipes


User = get_user_model()


class DashBoardView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        """
            overriding the get() method:
            - to pass a custome context in which, user_full_name and user_email in
            in the context.
            - also passing the all the swipe in the day.
            - current swipe status.
        """

        user_detail = {
            "user_full_name": f"{request.user.first_name} {request.user.last_name}",
            "user_email": request.user.email,
        }
        
        attendance = Attendance.objects.filter(user=request.user.id, date__date=datetime.now().date())
        if attendance.exists():
            attendance_status = "started"
            current_swipe = Swipes.objects.filter(attendance_id=attendance.first().id)
            
            if current_swipe.exists():
                swipe_status = current_swipe.last().swipe_status
                print(attendance_status)
                print(swipe_status)
                
                return render(request, "authentication/dashBoard.html", {"user_detail": user_detail,"attendance_status":attendance_status, "swipe_status":swipe_status, "todays_all_swipes": current_swipe[::-1]} )
            
        else:
            attendance_status = "not_started"
        
        return render(request, "authentication/dashBoard.html", {"user_detail": user_detail, "attendance_status":attendance_status} )
