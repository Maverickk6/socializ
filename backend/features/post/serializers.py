from rest_framework import serializers
from .models import Post
from features.comments.serializers import CommentSerializer


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    author_image = serializers.ReadOnlyField(source="author.image.url")
    author_id = serializers.ReadOnlyField(source="author.id")
    likes = serializers.SerializerMethodField()
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    def get_likes(self, obj):
        return [user.username for user in obj.likes.all()]


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'