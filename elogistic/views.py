from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import NetworkNode
from .serializers import NetworkNodeSerializer
from rest_framework.exceptions import PermissionDenied


class IsActiveUser(permissions.BasePermission):
    """
    Проверяет активность пользователя. Если неактивен, выбрасывает PermissionDenied (код 403).
    """
    def has_permission(self, request, view):
        if not request.user.is_active:
            raise PermissionDenied('Учетная запись не активна. Обратитесь к администратору.')
        return True


class NetworkNodeViewSet(viewsets.ModelViewSet):
    queryset = NetworkNode.objects.all().select_related('supplier').prefetch_related('products')
    serializer_class = NetworkNodeSerializer
    permission_classes = [permissions.IsAuthenticated, IsActiveUser]  # доступ только активным
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['country']  # фильтр по стране
    http_method_names = ['get', 'post', 'put', 'patch']  # запрещаем DELETE
