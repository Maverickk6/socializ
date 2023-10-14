from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User
from features.post.serializers import PostSerializer


class UsersSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    posts_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ("password",)

    def get_posts_count(self, obj):
        return obj.posts.count()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "bio",
            "image",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class ChangePasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(required=True, write_only=True, min_length=5)
    password2 = serializers.CharField(required=True, write_only=True, min_length=5)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        else:
            return data


class SearchUserSerializer(serializers.ModelSerializer):
    posts_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "image",
            "posts_count",
        )
    
    def get_posts_count(self, obj):
        return obj.posts.count()


class UserLoggedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "image",
        )


# Auth


class CustomTokenPairSerializer(TokenObtainPairSerializer):
    pass
