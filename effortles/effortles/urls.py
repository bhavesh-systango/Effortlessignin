from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from effortles import views


urlpatterns = [
    path('', RedirectView.as_view(url="/authentication/login")),
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('employee/', include('employee.urls')),
    path('attendance/', include('attendance.urls')),
    path('event/', include('event.urls')),
    path('api/', include('rest.urls')),
    path('attendanceRoundOff/', views.attendance_round_off, name="attendanceRoundOff" )
    
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns+=path('__debug__/', include('debug_toolbar.urls')),
    