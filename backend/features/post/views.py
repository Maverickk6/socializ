from .models import Post
from .serializers import PostSerializer, CreatePostSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from features.userAuth.pagination import CustomPagination
from rest_framework.views import APIView


def is_owner(request, instance):
    return request.user == instance.author or request.user.is_staff


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer

    def get_query_set(self):
        if self.queryset is None:
            self.queryset = Post.objects.all()
            return self.queryset
        else:
            return self.queryset

    def get_object(self, pk=None):
        return get_object_or_404(Post, pk=pk)

    def list(self, request):
        posts = self.serializer_class.Meta.model.objects.order_by("-id").all()
        paginator = CustomPagination()
        results = paginator.paginate_queryset(posts, request)

        posts_serializer = self.get_serializer(results, many=True)
        return paginator.get_paginated_response(posts_serializer.data)

    def create(self, request):
        post_serializer = CreatePostSerializer(data=request.data)
        if post_serializer.is_valid():
            post_serializer.save()
            return Response(post_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(post_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        post = self.get_object(pk=pk)
        post_serializer = self.serializer_class(post)
        return Response(post_serializer.data, status=status.HTTP_200_OK)

    def update_post(self, request, pk=None):
        post = self.get_object(pk=pk)
        if not is_owner(request, post):
            return Response(
                {"message": "You are not authorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            if "image" not in request.data or request.data["image"] == "":
                data = request.data.copy()
                current_image = post.image
                data["image"] = current_image

                post_serializer = PostSerializer(post, data=data)
                if post_serializer.is_valid():
                    post_serializer.save()
                    return Response(
                        {
                            "message": "post updated successfully",
                            "data": post_serializer.data,
                        },
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        post_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                post_serializer = PostSerializer(post, data=request.data)
                if post_serializer.is_valid():
                    post_serializer.save()
                    return Response(
                        {
                            "message": "Post successfully Updated",
                            "data": post_serializer.data,
                        }
                    )
                else:
                    return Response(
                        post_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )

    def delete_post(self, request, pk=None):
        post = self.get_object(pk=pk)
        if not is_owner(request, post):
            return Response(
                {"message": "You are not authorized to delete this post"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        else:
            post.delete()
            return Response(
                {"message": "Post deleted successfully"}, status=status.HTTP_200_OK
            )


class LikePostView(APIView):
    def post(self, request, id):
        try:
            post = get_object_or_404(Post, pk=id)
            post.likes.add(request.user)
            return Response({"message": "post liked!"}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(
                {"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )


class UnlikePostView(APIView):
    def post(self, request, id):
        try:
            post = get_object_or_404(Post, pk=id)
            post.likes.remove(request.user)
            return Response({"message": "Post unliked!"}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(
                {"message": "Post not found"}, status=status.HTTP_404_NOT_FOUND
            )
