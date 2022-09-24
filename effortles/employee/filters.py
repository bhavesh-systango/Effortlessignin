import django_filters
from django.contrib.auth import get_user_model


User = get_user_model()


class EmployeeListFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'first_name':['exact'],
            'last_name':['exact'],
            'date_joined':['date'],
            'email':['exact'],
            'user_type':['exact'],
            'created_at':['date'],
            'updated_at':['date'],
            'department_id':['exact'],
            'designation_id':['exact'],
            'reporting_manager':['exact']
        }
