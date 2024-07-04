from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, UsersRequests, IPAddressLog

admin.site.register([CustomUser, UsersRequests, IPAddressLog])




