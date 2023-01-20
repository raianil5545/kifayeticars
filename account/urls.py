from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from account import views

from .forms import PwdResetConfirmForm, PwdResetForm

app_name = "account"

urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("login/", views.LogInUserView.as_view(), name="login"),
    path("logout/", views.LogOutUserView.as_view(), name="logout"),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    path('dashboard', login_required(TemplateView.as_view(
        template_name="account/user/dashboard.html")), name='dashboard'),
    path('profile', login_required(TemplateView.as_view(template_name="account/user/profile.html")), name='profile'),
    path('profile/edit/<int:pk>', views.UserProfileUpdate.as_view(), name='edit-profile'),
    path('profile/delete/<int:pk>', views.UserProfileDeleteView.as_view(), name='delete-profile'),
    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name="account/user/password_reset_form.html",
                                              success_url='password_reset_email_confirm',
                                              email_template_name='account/user/password_reset_email.html',
                                              form_class=PwdResetForm), name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='account/user/password_reset_confirm.html',
                                                     success_url='/account/password_reset_complete/',
                                                     form_class=PwdResetConfirmForm),
         name="password_reset_confirm"),
    path('password_reset/password_reset_email_confirm/',
         TemplateView.as_view(template_name="account/user/password_reset_done.html"), name='password_reset_done'),
    path('password_reset_complete/',
         TemplateView.as_view(template_name="account/user/password_reset_complete.html"),
         name='password_reset_complete'),
]
