from rest_framework import viewsets, permissions
from .models import Formations
from .serializers import FormationsSerializer

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # SAFE_METHODS = GET, HEAD, OPTIONS -> accessible à tous
            return True
        # POST, PUT, PATCH, DELETE -> uniquement admin
        return request.user.is_authenticated and request.user.role == 'admin'


class FormationsView(viewsets.ModelViewSet):
    queryset = Formations.objects.all()
    serializer_class = FormationsSerializer
    permission_classes = [IsAdminOrReadOnly]