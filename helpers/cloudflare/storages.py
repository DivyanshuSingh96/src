# Why we are doing this?
# Because we want to customize the s3 storage instead of the default values

from storages.backends.s3 import S3Storage

class StaticFileStorage(S3Storage):
    # helpers.cloudflare.storages.StaticFileStorage
    location = "static"

class MediaFileStorage(S3Storage):
    # helpers.cloudflare.storages.MediaFileStorage
    location = "media"