from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from posts.models import Post, Group, Comment, User
from .serializers import (PostSerializer,
                          GroupSerializer,
                          CommentSerializer,
                          UserSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def update(self, request, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial
                                         )
        serializer.is_valid(raise_exception=True)
        if instance.author == self.request.user:
            self.perform_update(serializer)
            if getattr(instance, 'prefetched_obj', None):
                instance.prefetched_obj = {}
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, **kwargs):
        instance = self.get_object()
        if instance.author == self.request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_id = self.args
        return Comment.objects.filter(post=post_id)

    def perform_create(self, serializer):
        post = Post.objects.get(id=self.request.parser_context.get('args')[0])
        serializer.save(
            post=post,
            author=self.request.user
        )

    def retrieve(self, request, pk=None):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        partial = kwargs.pop('partial', False)
        queryset = Comment.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial
                                         )
        serializer.is_valid(raise_exception=True)
        if instance.author == self.request.user:
            self.perform_update(serializer)
            if getattr(instance, 'prefetched_obj', None):
                instance.prefetched_obj = {}
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        queryset = Comment.objects.all()
        instance = get_object_or_404(queryset, pk=pk)
        if instance.author == self.request.user:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
