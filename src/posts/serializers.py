from rest_framework import serializers

from .models import Post, PostLike


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created_at', 'updated_at', 'author')
        read_only_fields = ('created_at', 'updated_at', 'author')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['likes_qty'] = PostLike.objects.filter(post=instance.id).count()
        return representation


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('id', 'user', 'post', 'created_at')
        read_only = ('created_at',)
