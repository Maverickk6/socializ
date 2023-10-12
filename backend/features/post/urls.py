from django.urls import path
from .views import LikePostView, UnlikePostView

urlpatterns = [
    path('like/<int:postId>/', LikePostView.as_view(), name='like'),
    path('unlike/<int:postId>/', UnlikePostView.as_view(), name='unlike')
]
