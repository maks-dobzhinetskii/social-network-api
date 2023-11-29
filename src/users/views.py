from rest_framework.response import Response
from rest_framework import permissions, viewsets, status

from .models import User
from .serializers import UserListSerializer, UserRegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'create':
            return UserRegisterSerializer

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
