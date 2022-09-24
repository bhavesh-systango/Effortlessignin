from django.urls import path

from .views import SwipeMarkView, ShowCalender


urlpatterns = [
    path(
        "attendance/swipe/",
        SwipeMarkView.as_view(),
        name="mark_swipe",
    ),
    path(
        "attendance/calender",
        ShowCalender.as_view(),
        name="show_current_month_calender"
    ),
]
