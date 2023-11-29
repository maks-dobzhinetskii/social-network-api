from django.core.exceptions import ObjectDoesNotExist

from rest_framework.response import Response
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action


from .models import Post, PostLike
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'message': 'Post does not exist to be liked.'}, status=status.HTTP_400_BAD_REQUEST)

        post_like = PostLike.objects.filter(user=request.user, post=post).exists()
        if post_like:
            return Response({'message': 'Post is already liked.'}, status=status.HTTP_400_BAD_REQUEST)

        post_like = PostLike(user=request.user, post=post)
        post_like.save()
        return Response({'message': 'Post was liked.'}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def unlike(self, request, pk=None):
        try:
            post = Post.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response({'message': 'Post does not exist to be unliked.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            post_like = PostLike.objects.get(user=request.user, post=post)
        except ObjectDoesNotExist:
            return Response({'message': 'Post was not liked to be unliked'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            post_like.delete()
            return Response({'message': 'Post was unliked.'}, status=status.HTTP_204_NO_CONTENT)
