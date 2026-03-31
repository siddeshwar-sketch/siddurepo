from rest_framework import viewsets, permissions, authentication
from .models import Donation
from .serializers import DonationSerializer

class DonationViewSet(viewsets.ModelViewSet):
    serializer_class = DonationSerializer
    authentication_classes = [authentication.SessionAuthentication, authentication.BasicAuthentication]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff or user.role == user.Role.ADMIN:
                return Donation.objects.all().order_by('-created_at')
            return Donation.objects.filter(donor=user).order_by('-created_at')
        return Donation.objects.none()

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(donor=user)
