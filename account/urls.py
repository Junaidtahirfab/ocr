from django.urls import path
from account.views import *

urlpatterns = [
    path("send/otp/",                      SendOTPView.as_view(),             name='send-otp'),
    path("verify/otp/",                    VerifyOTPView.as_view(),           name='verify-otp'),
    path("user/register/",                 UserView.as_view(),                name='user-register'),
    path("login/",                         UserLoginView.as_view(),           name='login'),
    path("change/password/",               ChangePasswordView.as_view(),      name="change-password"),
    path("reset/password/",                ResetPasswordStep1View.as_view(),  name="reset-password-1"),
    path("reset/password/complete/",       ResetPasswordStep2View.as_view(),  name="reset-password-2"),
    path("role/",                          RoleListView.as_view(),            name='role-list'),
    path("user/",                          UserListView.as_view(),            name='user-create-list'),
    path("profile/",                       ProfileApiView.as_view(),          name='profile-view'),
    
    ]