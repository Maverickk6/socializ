from django.contrib import admin
from .models import Post

# Register your models here.


class PostAdmin(admin.ModelAdmin):
    items_display = ("author", "id",)
    ordering = ("-id",)


admin.site.register(Post, PostAdmin)
