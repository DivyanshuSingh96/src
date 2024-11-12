from django.db import models
from django.utils.safestring import mark_safe

# Create your models here.
class ImageView(models.Model):
    title = models.CharField(max_length=120)
    cloudflare_id = models.CharField(max_length=200)
    description = models.CharField(max_length=255, blank=True)
    image = models.ImageField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def image_display(self):
        if self.image:
            return mark_safe(
                f'<img src="{self.image.url}" style="width: 100px; height: 100px; border-radius: 10px; background-size: cover;">'
            )
        else:
            return "No Image Found"
    image_display.short_description = "Image"
    
    def __str__(self):
        return self.title