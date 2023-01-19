from django.urls import path

from account import views

app_name = "account"

urlpatterns = [
    path("register/", views.RegisterUserView.as_view(), name="register"),
    path("login/", views.LogInUserView.as_view(), name="login"),
    path("logout/", views.LogOutUserView.as_view(), name="logout"),
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
]
