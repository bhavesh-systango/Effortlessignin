import kronos
import calendar
import logging
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth import get_user_model
from attendance.models import Attendance
from employee.models import Salary, PaySlip


User = get_user_model()


@kronos.register('1 1 1 * *')
class Command(BaseCommand):
    help = "this command will generate the payslip of the current month"

    def handle(self, *args, **options):
        """
            function will generate the payslip 

            - get the total working day in the month
            - get attendance of all the user of current month
            - get all the salary from salary table
            - take out the distinct user from the query set

        """
        current_year = datetime.now().strftime("%Y")
        current_month = datetime.now().strftime("%m")

        current_month_calander = calendar.monthcalendar(
            int(current_year), int(current_month))

        working_day = 0

        for week in current_month_calander:
            for day_number, day in enumerate(week):
                if day_number != 5 and day_number != 6 and day != 0:
                    working_day += 1
                    
        all_attendance_of_current_month = Attendance.objects.filter(
            date__year=current_year, date__month=current_month)
        all_users = all_attendance_of_current_month.distinct(
            'user').values('user')

        for single_user in all_users:
            user_salary = Salary.objects.filter(
                user=single_user["user"]).order_by("-created_at").first()
            filtered_attendance_by_user = all_attendance_of_current_month.filter(
                user=single_user["user"])
            present_attendance = filtered_attendance_by_user.filter(
                attendance_status='present')
            half_day_attendance = filtered_attendance_by_user.filter(
                attendance_status='half_day_leave')

            if user_salary != None:
                payable_amount_per_day = user_salary.salary//working_day
                total_payable_amount = (len(present_attendance)*payable_amount_per_day)+(
                    len(half_day_attendance)*(payable_amount_per_day//2))
                user_payslip = PaySlip(
                    user=User(single_user["user"]), payslip=total_payable_amount)
                user_payslip.save()

            else:
                logging.info("users salary record not found")
