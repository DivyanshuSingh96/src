from django.db import models
from imageUpload.models import ImagePost

# Create your models here.
class Task(models.Model):
    key = models.CharField(max_length=255)
    keyId = models.CharField(max_length=255)

    def __str__(self):
        return self.key

class EncryptedImage(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    image_url = models.ForeignKey(ImagePost, blank=True, null=True, on_delete=models.SET_NULL)  # Stores the URL of the image
    is_encrypted = models.BooleanField(default=True)
    message = models.CharField(max_length=255)

    public_key = models.CharField(max_length=500)
    private_key = models.CharField(max_length=500)

    def __str__(self):
        return self.title