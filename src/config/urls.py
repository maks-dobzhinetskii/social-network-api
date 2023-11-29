from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/users/', include('users.urls', namespace='users')),
    path('api/posts/', include('posts.urls', namespace='posts')),
    path('api/analytics/', include('analytics.urls', namespace='analytics'))
]
