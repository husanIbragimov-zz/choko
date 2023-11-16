from rest_framework import generics, viewsets, views, mixins, status, filters, permissions
from .serializers import AdminCreateSerializer, AdminListSerializer, ClientCreateSerializer, ClientListSerializer, \
    AdminLoginSerializer
from django.contrib.auth.models import User
from .permissions import IsSuperUser
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


class AdminViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                   mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = AdminListSerializer
    ordering_fields = ['created_at']
    queryset = User.objects.all()
    permission_classes = [IsSuperUser]

    def get_queryset(self):
        return User.objects.filter(is_staff=True).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return AdminCreateSerializer
        return AdminListSerializer



class ClientViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                    mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = ClientListSerializer
    ordering_fields = ['created_at']
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return User.objects.filter(is_staff=False).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return ClientCreateSerializer
        return ClientListSerializer

    @action(methods=['get'], detail=False)
    def me(self, request):
        user = self.queryset.filter(id=request.user.id).first()
        if user:
            serializer = self.serializer_class(request.user)
            return Response(serializer.data)
        return Response({"message": "Anonymous user"}, status=status.HTTP_404_NOT_FOUND)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = AdminLoginSerializer

    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'success': False, 'message': f'Password or phone number invalid'},
                            status=status.HTTP_400_BAD_REQUEST)

