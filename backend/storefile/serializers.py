from rest_framework import serializers
from .models import Snippet, File


class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style',)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'name', 'user', 'size', 'created']
        read_only_fields = ('user', 'size', 'name', 'created')
