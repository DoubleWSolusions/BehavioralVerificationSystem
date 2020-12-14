from rest_framework import serializers
from .models import *


class ExtractedFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtractedFeatures
        fields = '__all__'
