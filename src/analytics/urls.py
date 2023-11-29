from django.urls import path

from . import views

app_name = 'analytics'

urlpatterns = [
    path('post-likes/', views.get_likes_analytics, name='get-likes-analytics'),
    path('users/<int:pk>/', views.get_user_activity_analytics, name='get-user-activity-analytics')
]
