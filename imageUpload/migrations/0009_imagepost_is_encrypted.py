# Generated by Django 5.1.2 on 2024-11-11 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("imageUpload", "0008_alter_imagepost_cloudflare_path"),
    ]

    operations = [
        migrations.AddField(
            model_name="imagepost",
            name="is_encrypted",
            field=models.BooleanField(default=False),
        ),
    ]
