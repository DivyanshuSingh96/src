# Generated by Django 5.1.2 on 2024-11-11 11:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "imageUpload",
            "0006_remove_imagepost_image_imagepost_cloudflare_path_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="imagepost",
            name="url_expiration",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
