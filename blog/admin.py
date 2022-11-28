from django.contrib import admin

# Register your models here.

from .models import UserRegister, blogg
admin.site.register((UserRegister))
admin.site.register((blogg))

