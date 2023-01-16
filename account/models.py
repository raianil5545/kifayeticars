from datetime import datetime

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, first_name: str, email: str,
                    password: str = None, last_name: str = None,
                    is_staff=False, is_superuser=False) -> "AppUser":
        if not email:
            raise ValueError("Email is required Field")
        if not first_name:
            raise ValueError("First Name is required Field")
        email = self.normalize_email(email)
        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          is_staff=is_staff,
                          is_superuser=is_superuser,
                          is_active=True)
        user.set_password(password)
        user.save()
        return user


    def create_superuser(self, email:str, first_name:str, 
                         last_name:str, password:str) -> "AppUser":
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        return user        


class AppUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("email address"), 
                              unique=True)
    first_name = models.CharField(max_length=150,
                                  verbose_name="first name")
    last_name = models.CharField(max_length=150,
                                 verbose_name="last name",
                                 blank=True,
                                 null=True)
    password = models.CharField(_("password"),
                                max_length=250)
    date_joined = models.DateTimeField(auto_now_add=datetime.now())
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    object = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name","last_name",]
    
    
    def __str__(self):
        return self.email
    

    