from django.contrib import admin
from .models import ImageView
from imageUpload.forms import ImagePostForm

# Register your models here.
@admin.register(ImageView)
class ImageViewAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_display', 'uploaded_at')
    # readonly_fields = ['image_display']
    # form = ImagePostForm