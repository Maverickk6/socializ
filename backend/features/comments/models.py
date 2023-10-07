from django.db import models
from features.post.models import Post
from django.contrib.auth import get_user_model

# Create your models here.


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"comment by: {self.author.username} on {self.post.title}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
