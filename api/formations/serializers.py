from rest_framework import serializers
from .models import Formations

class FormationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formations
        fields = ['id', 'title', 'description', 'prix', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']