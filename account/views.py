from typing import Any

from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic.edit import DeleteView, FormView, UpdateView

from account.forms import RegisterForm, UserLoginForm, UserUpdateForm

from .models import AppUser
from .tokens import account_activation_token


class RegisterUserView(FormView):
    template_name = 'account/registration/register.html'
    form_class = RegisterForm
    success_url = '/account/login/'

    def form_valid(self, form):
        registrationForm = form
        user = registrationForm.save(commit=False)
        user.email = registrationForm.cleaned_data["email"]
        user.set_password(registrationForm.cleaned_data["password"])
        user.is_active = False
        if registrationForm.cleaned_data["email"].split("@")[1] == "kifayeticar.com":
            user.is_staff = True
        else:
            user.is_staff = False
        user.save()
        user = AppUser.objects.get(email=registrationForm.cleaned_data["email"])
        if not user.is_staff:
            customer_group = Group.objects.get_or_create(name="Customer")
            user.groups.add(customer_group[0])
        else:
            staff_group = Group.objects.get_or_create(name="Staff")
            user.groups.add(staff_group[0])
        user.save()
        current_site = get_current_site(self.request)
        subject = 'Activate your Account'
        message = render_to_string('account/registration/account_activation_email.html', {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
        user.email_user(subject=subject, message=message)
        return super().form_valid(form)


class LogInUserView(auth_views.LoginView):
    template_name = "account/registration/login.html"
    form_class = UserLoginForm

    def form_valid(self, form):
        """Security check completed. add the token."""
        request_data = form.cleaned_data
        user = AppUser.objects.all().filter(email=request_data["username"]).values()
        user = user[0]
        self.request.session.setdefault('user_email', user["email"])
        self.request.session.setdefault('is_staff', user["is_staff"])
        self.request.session.setdefault('user_id', user["id"])
        return super().form_valid(form)


class LogOutUserView(auth_views.LogoutView):
    def post(self, request, *args, **kwargs):
        del request.session["user_email"]
        del request.session["is_staff"]
        del request.session["user_id"]
        return super().post(request, *args, **kwargs)


def account_activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = AppUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')


class UserProfileUpdate(UpdateView):
    template_name = 'account/user/updateprofile.html'
    success_url = '/account/dashboard'
    queryset = AppUser.objects.all()
    form_class = UserUpdateForm


class UserProfileDeleteView(DeleteView):
    @method_decorator(login_required)
    def post(self, request, *args: Any, **kwargs: Any):
        user = AppUser.objects.get(email=request.user)
        user.is_active = False
        user.save()
        return render(request, template_name="account/user/delete_confirm.html")
