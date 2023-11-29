from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Title')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PostLike(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='User')
    post = models.ForeignKey('Post', on_delete=models.CASCADE, verbose_name='Post')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f'{self.user} likes {self.post}'
