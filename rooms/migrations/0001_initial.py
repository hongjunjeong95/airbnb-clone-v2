# Generated by Django 2.2.5 on 2021-01-18 08:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HouseRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=80)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=140)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('city', models.CharField(max_length=140)),
                ('address', models.CharField(max_length=140)),
                ('price', models.IntegerField()),
                ('guests', models.IntegerField()),
                ('bedrooms', models.IntegerField()),
                ('beds', models.IntegerField()),
                ('bathrooms', models.IntegerField()),
                ('description', models.TextField()),
                ('instant_book', models.BooleanField(default=False)),
                ('amenities', models.ManyToManyField(blank=True, related_name='rooms', to='rooms.Amenity')),
                ('facilities', models.ManyToManyField(blank=True, related_name='rooms', to='rooms.Facility')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to=settings.AUTH_USER_MODEL)),
                ('house_rules', models.ManyToManyField(blank=True, related_name='rooms', to='rooms.HouseRule')),
                ('room_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='rooms', to='rooms.RoomType')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]