import uuid
import random
import string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import CustomManager

# Create your models here.
def rand_name():
    name_length = 10
    while True:
        name = "".join(random.choices(string.ascii_uppercase + string.digits, k = name_length))
        if not CustomUser.objects.filter(username=name).exists():
            return name

class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(_("email address"), unique=True)
    username = models.CharField(default=rand_name, max_length=255)
    avatar = models.ImageField(upload_to="avatar", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    is_verify = models.BooleanField(default=False)
    location = models.CharField(null=True, blank=True, max_length=189)
    bio = models.TextField(null=True, blank=True)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomManager()
    
    def __str__(self):
        return self.username