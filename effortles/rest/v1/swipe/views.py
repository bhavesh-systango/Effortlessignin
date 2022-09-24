from datetime import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend

from attendance.models import Attendance, Swipes
from .serializers import SwipeSerializer


User = get_user_model()


class MakeSwipeViewSet(viewsets.ModelViewSet):
    queryset = Swipes.objects.all()
    serializer_class = SwipeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['attendance_id', 'time_of_swipe',
                        'swipe_status', 'created_at', 'updated_at']
    http_method_names = ['get', 'post']

    def get_queryset(self):
        if self.request.method == "GET":
            queryset = Swipes.objects.all()

        else:
            queryset = Swipes.objects.filter(user=self.request.user.id).all()

        create_at = self.request.query_params.get('create_at')
        update_at = self.request.query_params.get('update_at')

        if create_at is not None:
            entered_date = create_at.split("-")
            entered_year = int(entered_date[0])
            entered_month = int(entered_date[1])
            entered_day = int(entered_date[2])
            queryset = queryset.filter(
                created_at__date=f"{entered_year}-{entered_month}-{entered_day}")

        if update_at is not None:
            entered_date = update_at.split("-")
            entered_year = int(entered_date[0])
            entered_month = int(entered_date[1])
            entered_day = int(entered_date[2])
            queryset = queryset.filter(
                updated_at__date=f"{entered_year}-{entered_month}-{entered_day}")

        return queryset

    def create(self, request, *args, **kwargs):
        '''
            overrided created method for following:

            - getting attendance object of user 
            - if object exist then the swipe will be marked
            - else an object will be made and then the swipe will be marked
        '''

        attendance = Attendance.objects.filter(
            user=User(request.data['user'][0]), date__date=datetime.now().date())
        data_dict = request.data.copy()

        if not attendance.exists():
            todays_attendance = Attendance(
                user=User(request.data['user'][0]), swipe_status="swiped_in")
            todays_attendance.save()

            data_dict.update({
                'attendance_id': todays_attendance.id,
                'time_of_swipe': datetime.now(),
                'swipe_status': 'swiped_in',
            })
        else:

            current_swipe = Swipes.objects.filter(
                attendance_id=attendance.first().id).last()

            if current_swipe == None:
                data_dict.update({
                    'attendance_id': attendance.first().id,
                    'time_of_swipe': datetime.now(),
                    'swipe_status': 'swiped_in',
                })

            elif current_swipe.swipe_status != "swiped_in":
                data_dict.update({
                    'attendance_id': attendance.first().id,
                    'time_of_swipe': datetime.now(),
                    'swipe_status': 'swiped_in',
                })

            else:
                data_dict.update({
                    'attendance_id': attendance.first().id,
                    'time_of_swipe': datetime.now(),
                    'swipe_status': 'swiped_out',
                })

        serializer = self.get_serializer(data=data_dict)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
