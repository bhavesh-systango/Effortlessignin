from django import forms
from django.contrib.auth import get_user_model
from authentication.models import Department, Designation 


User = get_user_model()

class AddUserForm(forms.ModelForm):
    USER_TYPE=[
        ("admin", "admin"),
        ("regular", "regular"),
    ]

    user_type = forms.CharField(widget=forms.Select(choices=USER_TYPE))
    department_id = forms.ModelChoiceField(
        queryset=Department.objects.all(), widget=forms.Select())
    designation_id = forms.ModelChoiceField(
        queryset=Designation.objects.all(), widget=forms.Select())
    date_joined = forms.DateField(
        widget=forms.DateInput(attrs={"type":"date"}))

    class Meta:

        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "user_type",
            "department_id",
            "designation_id",
            "date_joined",
        ]


class EditUserForm(AddUserForm):
    date_joined = forms.DateField(
        widget=forms.DateInput(attrs={"type":"date"}))
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "user_type",
            "department_id",
            "designation_id",
            "date_joined",
            "reporting_manager",
        ]
        