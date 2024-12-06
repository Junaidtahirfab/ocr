from rest_framework import serializers
from .models import Company, Folder, CompanyFile

class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Folder
        fields = "__all__"
        read_only_fields = ("created_by", "created_at")


class CompanyFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyFile
        fields = "__all__"
        read_only_fields = ("uploaded_by", "uploaded_at")
