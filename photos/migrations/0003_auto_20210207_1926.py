# Generated by Django 2.2.5 on 2021-02-07 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0002_photo_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='file',
            field=models.ImageField(blank=True, upload_to='room_photos'),
        ),
    ]