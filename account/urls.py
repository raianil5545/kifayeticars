from django.urls import path

from account.views import LogInUserView, LogOutUserView, RegisterUserView

app_name =  "account"


urlpatterns = [
    path("register/", RegisterUserView.as_view() , name="register"),
    path("login/", LogInUserView.as_view() , name="login"),
    path("logout/", LogOutUserView.as_view(), name="logout"),
]
