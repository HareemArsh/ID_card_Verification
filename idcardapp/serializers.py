from rest_framework import serializers
from .models import ScannedIDCard

class ScannedIDCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScannedIDCard
        fields = '__all__'
