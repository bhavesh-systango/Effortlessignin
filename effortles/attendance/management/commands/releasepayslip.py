import logging
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError
# from django.contrib.auth import get_user_model
from employee.models import PaySlip

# User = get_user_model()


class Command(BaseCommand):
    help = "command to make the payslip status change to relase"

    def add_arguments(self, parser):
        parser.add_argument('year', type=int)
        parser.add_argument('month', type=int)

    def handle(self, *args, **options):
        """
            function will mark all the payslip is_release to true fron false.

            - take year and month form the argument
            - take out all PaySlip object
            - filter all the PaySlip object by year and month

        """

        all_pay_slips = PaySlip.objects.filter(created_at__year=str(
            options['year']), created_at__month=str(options['month']))
        all_pay_slips.update(is_released=True)
