from .serializers import GetInTouchSerializer, LocationSerializer, SubscribeSerializer
from apps.contact.models import GetInTouch, Location, Subscribe
from api.account.permissions import IsSuperUser
from rest_framework import viewsets, mixins, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend


class GetInTouchViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                        mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = GetInTouchSerializer
    queryset = GetInTouch.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['status', 'first_name', 'last_name', 'phone_number', 'message']
    ordering_fields = ['status', 'phone_number']
    permission_classes = [IsSuperUser]

    def get_permissions(self):
        if self.action == 'list' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
