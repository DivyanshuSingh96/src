from pathlib import Path
import uuid

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.safestring import mark_safe

from imageViewer.models import ImageView
from imageViewer.services import get_image_url_from_cloudflare, upload_image_to_cloudflare

# Create your models here.
class ImagePost(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=255, blank=True)
    # This will handle the file upload
    image_file = models.ImageField(upload_to='temp/', null=True)
    # This will store the Cloudflare path
    cloudflare_path = models.URLField(max_length=500, blank=True)
    # cloudflare_url = models.URLField()
    author = models.CharField(max_length=50, null=True, blank=True)
    url_expiration = models.DateTimeField(default=timezone.now)
    is_encrypted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.image_file and not self.cloudflare_path:
            try:
                # Upload to Cloudflare and get the path
                file_url = upload_image_to_cloudflare(
                    instance=self,
                    image_file=self.image_file
                )
                if file_url:
                    self.cloudflare_path = file_url
                    # Clear the image_file after successful upload
                    self.image_file = None
            except Exception as e:
                print(f"Error uploading to Cloudflare: {str(e)}")
        
        super().save(*args, **kwargs)

    def image_display(self):
        """Display image in admin panel"""
        if self.cloudflare_path:
            # Get complete URL using your function
            full_url = get_image_url_from_cloudflare(self.cloudflare_path)
            print(full_url)

            return mark_safe(
                f'<img src="{full_url}" '
                f'style="width: 150px; height: 150px; border-radius: 10px; background-size: cover;">'
            )
        return "No Image Found"
    
    image_display.short_description = "Image"
    image_display.allow_tags = True

    def get_image_url(self):
        """Helper method to get the full Cloudflare R2 URL"""
        if self.cloudflare_path:
            return get_image_url_from_cloudflare(self.cloudflare_path)
        return None

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-timestamp']