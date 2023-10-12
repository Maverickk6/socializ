from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    items_display = ("username", "email", "id",)
    ordering = ("id",)


admin.site.register(User, UserAdmin)
