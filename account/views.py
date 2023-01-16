from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth import views as auth_views
from django.views.generic.edit import FormView
from django.contrib.auth.models import Group


from account.forms import LogInForm, RegisterForm

from .models import AppUser


class RegisterUserView(FormView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = '/user/login/'
    def form_valid(self, form):
        user_data = form.cleaned_data
        if user_data["email"].split("@")[1] == "kifayeticar.com":
            user_data["is_staff"] = True
        else:
            user_data["is_staff"] = False
        user = AppUser(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            is_staff=user_data["is_staff"]
        )
        if user_data["password"] is not None:  
            user.set_password(user_data["password"])
            user.save()
        new_user = AppUser.object.get(email=user_data["email"])
        if not new_user.is_staff:
            customer_group = Group.objects.filter(name="Customer")
            new_user.groups.add(customer_group.values()[0]["id"])
        staff_group = Group.objects.filter(name="Staff")
        new_user.groups.add(staff_group.values()[0]["id"])
        new_user.save()
        return super().form_valid(form) 


class LogInUserView(auth_views.LoginView):
    template_name = "users/login.html"
    
    
    def get_success_url(self):
        return "/"

    def form_valid(self, form):
        """Security check completed. add the token."""
        request_data = form.cleaned_data
        user = AppUser.object.all().filter(email=request_data["username"]).values()
        user = user[0]
        self.request.session.setdefault('user_email', user["email"])
        self.request.session.setdefault('is_staff', user["is_staff"])
        self.request.session.setdefault('user_id', user["id"])
        return super().form_valid(form)


class LogOutUserView(auth_views.LogoutView):
    def get_success_url(self):
        return "/"
    
    
    def post(self, request, *args, **kwargs):
        del request.session.user_email
        del request.session.is_staff
        del request.session.user_id
        return super().post(request, *args, **kwargs)
    