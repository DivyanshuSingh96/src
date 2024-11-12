from rest_framework import serializers
from .models import Task, EncryptedImage

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

class EncryptedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EncryptedImage  # Model to serialize
        fields = ['title', 'author', 'image_url', 'is_encrypted', 'message', 'public_key', 'private_key']  # Fields to include

    def create(self, validated_data):
        """
        Custom method for creating an EncryptedImage instance.
        """
        return EncryptedImage.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Custom method for updating an existing EncryptedImage instance.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.is_encrypted = validated_data.get('is_encrypted', instance.is_encrypted)
        instance.message = validated_data.get('message', instance.message)
        instance.public_key = validated_data.get('public_key', instance.public_key)
        instance.private_key = validated_data.get('private_key', instance.private_key)
        instance.save()
        return instance