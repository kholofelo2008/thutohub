from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # your custom User model

# Register your custom User with the full UserAdmin interface
admin.site.register(User, UserAdmin)