from rest_framework import serializers
from .models import *
    
class FileManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileManager
        fields = "__all__"
