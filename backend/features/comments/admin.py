from django.contrib import admin
from .models import Comment

# Register your models here.


class CommentAdmin(admin.ModelAdmin):
    ordering = ("-id",)


admin.site.register(Comment, CommentAdmin)
