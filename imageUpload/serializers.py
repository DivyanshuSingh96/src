from rest_framework import serializers

from .models import ImagePost
from imageViewer.services import get_image_url_from_cloudflare

class ImagePostSerializer(serializers.ModelSerializer):
    # image_file = serializers.SerializerMethodField()
    image_file = serializers.ImageField(required=True)

    class Meta:
        model = ImagePost
        fields = ["id", "title", "author", "cloudflare_path", "image_file", "is_encrypted"]

    def create(self, validated_data):
        # Use validated data to create and return the ImagePost instance
        return ImagePost.objects.create(**validated_data)

    # def get_image_file(self, obj):
    #     return get_image_url_from_cloudflare(obj.cloudflare_path) if obj.cloudflare_path else None
