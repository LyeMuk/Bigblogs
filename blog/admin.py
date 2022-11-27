from django.contrib import admin

# Register your models here.

from .models import UserRegister
admin.site.register((UserRegister))
