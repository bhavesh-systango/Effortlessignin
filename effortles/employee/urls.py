from django.urls import path
from django.contrib.auth import get_user_model
from .views import ViewAllEmpoyeesView, AddEmployeeView, EditEmployee, EmployeeUnderMe, EmployeeDetail


User = get_user_model()


urlpatterns = [
    
    path('employee/',
        ViewAllEmpoyeesView.as_view(),
        name="view_all_employee"
    ),
    path('employee/underme',
        EmployeeUnderMe.as_view(),
        name='employee_under_me'
    ),
    path('employee/create',
        AddEmployeeView.as_view(),
        name="add_employee"
    ),
    path('employee/<int:pk>/detail', 
        EmployeeDetail.as_view(),
        name="employee_detail"
    ),
    path('editemployee/<int:pk>/update',
        EditEmployee.as_view(),
        name="edit_employee"
    ),
    
]
