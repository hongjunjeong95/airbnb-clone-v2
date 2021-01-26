# Generated by Django 2.2.5 on 2021-01-26 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_secret',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='currency',
            field=models.CharField(choices=[('KRW', 'KRW'), ('USD', 'USD')], max_length=3),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=6),
        ),
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.CharField(choices=[('KR', 'Korean'), ('EN', 'English')], max_length=2),
        ),
    ]