from django import forms

from .models import ImagePost
from imageViewer.services import (
    upload_image_to_cloudflare,
    get_image_url_from_cloudflare)

class ImagePostForm(forms.ModelForm):
    image_file = forms.ImageField(required=True)  # Temporary field for file upload

    class Meta:
        model = ImagePost
        fields = ['author', 'title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'content': forms.Textarea(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
            'author': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border rounded-lg'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        image_file = self.cleaned_data.get('image_file')
        
        if image_file:
            print(f"Image Uploading to R2: {image_file.name}")
            file_url = upload_image_to_cloudflare(instance=instance, image_file=image_file)

            if file_url:
                print(f"File URL: {file_url}")
                instance.image = file_url  # Store the path returned by upload_image_to_cloudflare
            else:
                raise forms.ValidationError("Failed to upload image to Cloudflare R2")
        
        if commit:
            instance.save()
        
        return instance