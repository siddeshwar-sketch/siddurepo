from rest_framework import serializers
from .models import Campaign, Category
from accounts.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CampaignSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    progress_percentage = serializers.ReadOnlyField()
    is_funded = serializers.ReadOnlyField()

    class Meta:
        model = Campaign
        fields = '__all__'
        read_only_fields = ('owner', 'raised_amount', 'status', 'approved', 'progress_percentage', 'is_funded')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return super().create(validated_data)
