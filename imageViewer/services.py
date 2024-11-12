import uuid

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def upload_image_to_cloudflare(instance, image_file, is_encrypted=False):
    filename = image_file.name
    instance_id = instance.id

    if not instance.id:
        instance_id = "0"

    folder_name = f"images/{instance_id}/"

    if is_encrypted:
        folder_name = f"images/{int(instance_id) + 1}/"

    try:
        unique_fname = str(uuid.uuid1())
        ext = filename.split(".")[-1]
        new_filename = f"{folder_name}{unique_fname}.{ext}"

        path = default_storage.save(new_filename, ContentFile(image_file.read()))
        file_url = default_storage.url(path)
        return file_url
    except Exception as e:
        print(f"Error uploading image to Cloudflare R2 {str(e)}")
        return None


def get_image_url_from_cloudflare(cloudflare_id):
    # bucket_name = settings.CLOUDFLARE_R2_BUCKET
    # bucket_endpoint = settings.CLOUDFLARE_R2_BUCKET_ENDPOINT
    image_url = cloudflare_id
    return image_url