from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

# grab the custom user model
User = get_user_model()


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email']


# Register your models here.
admin.site.register(User, CustomUserAdmin)
