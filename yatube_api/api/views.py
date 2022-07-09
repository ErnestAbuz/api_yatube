from rest_framework import permissions, viewsets
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from posts.models import Post, Group, Comment, User
from .serializers import (PostSerializer,
                          GroupSerializer,
                          CommentSerializer,
                          UserSerializer)
from .permissions import AuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated, AuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, AuthorOrReadOnly]

    def get_post(self):
        pk = self.kwargs.get('post_id')
        return get_object_or_404(Post, id=pk)

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
