from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkNode
from .serializers import NetworkNodeSerializer

class IsActiveUser(permissions.BasePermission):
    """
    Разрешение только для активных пользователей.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_active)


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all().select_related('supplier').prefetch_related('products')
    serializer_class = NetworkNodeSerializer
    permission_classes = [IsActiveUser]  # доступ только активным
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['country']  # фильтр по стране
    http_method_names = ['get', 'post', 'put', 'patch']  # запрещаем DELETE
