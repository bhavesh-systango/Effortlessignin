from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.base import TemplateView
from .views import DashBoardView
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordResetView,
    PasswordChangeDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)


urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="authentication/login.html",
            next_page="/authentication/dashboard",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(
            next_page="/authentication/login",
        ),
        name="logout",
    ),
    path("dashboard/", DashBoardView.as_view(), name="dashboard"),
    path(
        "changepassword/",
        PasswordChangeView.as_view(
            template_name="authentication/passwordChange.html",
            success_url="/authentication/changepasswordsuccess",
        ),
        name="changepassword",
    ),
    path(
        "changepasswordsuccess/",
        TemplateView.as_view(template_name="authentication/passwordChangeSucess.html"),
        name="changepasswordsuccess",
    ),
    path(
        "resetpassword/",
        PasswordResetView.as_view(
            template_name="authentication/forgotPassword.html",
            success_url="/authentication/resetpasswordemailsent",
        ),
        name="resetpassword",
    ),
    path(
        "resetpasswordemailsent/",
        PasswordChangeDoneView.as_view(
            template_name="authentication/passwordResetDone.html",
        ),
        name="resetpasswordemailsent",
    ),
    path(
        "reset/<uidb64>/<token>",
        PasswordResetConfirmView.as_view(
            template_name = "authentication/resetPassword.html",
            success_url = "/authentication/resetpasswordcomplete"
        ),
        name="password_reset_confirm",
    ),
    path(
        "resetpasswordcomplete/",
        PasswordResetCompleteView.as_view(
            template_name="authentication/passwordResetComplete.html",
        ),
        name = "resetpasswordcompletes",
    ),
]
