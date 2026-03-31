from rest_framework import serializers
from .models import Donation
from accounts.serializers import UserSerializer

class DonationSerializer(serializers.ModelSerializer):
    donor_info = serializers.SerializerMethodField()

    class Meta:
        model = Donation
        fields = '__all__'
        read_only_fields = ('donor', 'status', 'payment_id', 'created_at')

    def get_donor_info(self, obj):
        if obj.is_anonymous:
            return {"name": "Anonymous"}
        if obj.donor_name:
            return {"name": obj.donor_name}
        if obj.donor:
            return {"name": obj.donor.get_full_name() or obj.donor.username}
        return {"name": "Guest"}

    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['donor'] = request.user
            # Pre-fill name and email from user if not provided
            if not validated_data.get('donor_name'):
                validated_data['donor_name'] = request.user.get_full_name() or request.user.username
            if not validated_data.get('donor_email'):
                validated_data['donor_email'] = request.user.email
        return super().create(validated_data)
