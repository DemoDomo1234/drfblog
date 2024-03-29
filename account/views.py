from rest_framework.viewsets import ModelViewSet
from .models import User
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .permissions import UserPermission
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


class UserView(ModelViewSet):
    '''
    You can perform CRUD operations and register on users in this view
    '''
    model = User
    serializer_class = UserSerializer
    queryset = User.objects.all()

    # set permission for this view
    def get_permissions(self):
        if self.action in ['destroy', 'partial_update', 'update', 'retrieve']:
            permission_classes = [UserPermission]
        else:
            permission_classes = []

        return [permission() for permission in permission_classes]
        
    def perform_create(self, serializer):
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    def perform_update(self, serializer):
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


class UserFollowView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        request_user = request.user
        user = User.objects.get(id=pk)
        message = 'error'
        if user != None and user.is_active:
            if request_user not in user.follower.all():
                user.follower.add(request_user)
                message = 'You followed this user'
            else:
                user.follower.remove(request_user)
                message = 'You un followed this user'
        else:
            message = 'not find'
        return Response(message)


class UserNotificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        request_user = request.user
        user = User.objects.get(id=pk)
        message = 'error'
        if user != None and user.is_active:
            if request_user not in user.notifications.all():
                user.notifications.add(request_user)
                message = "You have turned on this user's notification"
            else:
                user.notifications.remove(request_user)
                message = "You have turned off this user's notification"
        else:
            message = 'not find'
        return Response(message)
