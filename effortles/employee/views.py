import secrets
import string
from decouple import config
from typing import Protocol
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView 
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from authentication.models import Department, Designation
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .forms import AddUserForm, EditUserForm
from .filters import EmployeeListFilter
from .tasks import user_created_email_send


User = get_user_model()


class ViewAllEmpoyeesView(LoginRequiredMixin, ListView):
    template_name = "employee/view_all_employee.html"
    model = User
    context_object_name = "employees" 

    
    def get_context_data(self, **kwargs):
        current_user_id = self.request.user.id
        current_user = User.objects.filter(id=current_user_id).first()

        context = super().get_context_data(**kwargs)

        filter_object = EmployeeListFilter(self.request.GET, queryset=self.get_queryset())
        context['filter_object'] = filter_object
        context.update({'current_user':current_user})

        return context


class AddEmployeeView(LoginRequiredMixin, CreateView):

    model = User
    form_class = AddUserForm
    template_name = "employee/add_employee.html"


    def post(self, request):
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        user_type = request.POST["user_type"]
        department_id = Department(int(request.POST["department_id"]))
        designation_id = Designation(int(request.POST["designation_id"]))
        date_joined = request.POST["date_joined"]
        password = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
                                                for i in range(8))    
        
        try:
            new_user = User()
            
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.email = email
            new_user.user_type = user_type
            new_user.department_id = department_id
            new_user.designation_id = designation_id
            new_user.date_joined = date_joined
            new_user.set_password(password) 

            new_user.save()

            protocol = "http"
            domain = config('PASSWORD_RESET_LINK_EMAIL_DOMAIN')
            uid = urlsafe_base64_encode(force_bytes(new_user.id))
            token = default_token_generator.make_token(new_user)


        except Exception as e:
            print(e)

        else:
            user_created_email_send.delay(first_name, last_name, email, uid, token, protocol, domain)

        return redirect("/employee/employee")


class EditEmployee(LoginRequiredMixin, UpdateView):

    model = User
    template_name = "employee/edit_employee.html"
    form_class = EditUserForm
    success_url = "/employee/employee"


class EmployeeUnderMe(LoginRequiredMixin, ListView):
    model = User
    template_name = "employee/employees_under_me.html"
    context_object_name = "employee_under_me"

    def get_queryset(self):
        return User.objects.filter(reporting_manager = self.request.user.pk)


class EmployeeDetail(LoginRequiredMixin, DetailView):
    template_name = "employee/employee_detail.html"
    model = User
    context_object_name= "employee_detail"
    