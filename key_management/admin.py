from django.contrib import admin

from .models import EncryptedImage
# from imageViewer.models import ImageView

# Register your models here.
@admin.register(EncryptedImage)
class EncryptedImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'image_url', "message", 'is_encrypted', "private_key", "public_key"]
    readonly_fields = ["image_url", "is_encrypted"]
    search_fields = ['title', 'content', 'author', "message"]
    list_filter = ['author', "title"]