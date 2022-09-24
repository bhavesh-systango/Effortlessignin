from django.db import models
from django.contrib.auth import get_user_model
from django.forms import BooleanField


User = get_user_model()


class Salary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    salary = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)+"__"+str(self.user)


class PaySlip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_released = models.BooleanField(default=False)
    payslip = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.pk)+"__"+str(self.user)+"__"+str(self.created_at)
