# Generated by Django 2.2.5 on 2021-01-26 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210126_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='login_method',
            field=models.CharField(choices=[('email', 'Email'), ('github', 'Github'), ('kakao', 'Kakao')], default='email', max_length=6),
        ),
    ]
