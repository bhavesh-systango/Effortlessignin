from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateUserForm(UserCreationForm):
    
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
