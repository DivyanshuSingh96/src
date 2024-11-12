from django.contrib import admin

from imageUpload.models import ImagePost
# from imageViewer.models import ImageView
from .forms import ImagePostForm
from imageViewer.services import upload_image_to_cloudflare

# Register your models here.
@admin.register(ImagePost)
class ImagePostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'timestamp', 'image_display']
    readonly_fields = ['image_display', 'timestamp', 'updated', "cloudflare_path", "url_expiration", "is_encrypted"]
    search_fields = ['title', 'content', 'author']
    list_filter = ['timestamp', 'author']

    fieldsets = (
        (None, {
            'fields': ('title', 'author', 'content', 'description')
        }),
        ('Image', {
            'fields': ('image_file', 'cloudflare_path', 'image_display', "is_encrypted")
        }),
        ('Timestamps', {
            'fields': ('timestamp', 'updated', "url_expiration"),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if 'image' in form.changed_data:
            image_file = form.cleaned_data.get('image')
            if image_file:
                file_url = upload_image_to_cloudflare(obj, image_file)
                if file_url:
                    obj.cloudflare_path = file_url
                    obj.image_file = image_file
        
        super().save_model(request, obj, form, change)