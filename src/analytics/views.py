from datetime import datetime
from django.db.models.functions import TruncDate
from django.db.models import Count
from django.contrib.auth import get_user_model

from django.apps import apps

from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes


from .serializers import UserActivitySerializer


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_likes_analytics(request):
    date_format = '%Y-%m-%d'
    date_from = request.query_params.get('date_from')
    date_to = request.query_params.get('date_to')

    if not date_from or not date_to:
        return Response({'message': 'Request should contain date_from and date_to query params.'},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        if datetime.strptime(date_from, date_format) > datetime.strptime(date_to, date_format):
            return Response({'message': 'date_from should be less or equal than date_to.'},
                            status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'message': f'date_from and date_to should have {date_format} date format.'},
                        status=status.HTTP_400_BAD_REQUEST)

    post_likes_qty = apps.get_model('posts', 'PostLike').objects.filter(created_at__range=[date_from, date_to]).count()

    post_likes_by_dates = (apps.get_model('posts', 'PostLike').objects
                           .filter(created_at__gte=date_from, created_at__lte=date_to)
                           .annotate(date=TruncDate('created_at'))
                           .values('date')
                           .annotate(count=Count('id')).order_by('date'))

    return Response({'post_likes_qty': post_likes_qty, 'post_likes_by_dates': post_likes_by_dates})


@api_view(['GET'])
@permission_classes([permissions.IsAdminUser])
def get_user_activity_analytics(request, pk=None):
    user = get_user_model().objects.get(pk=pk)
    serializer = UserActivitySerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)
