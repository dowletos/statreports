# Generated by Django 4.1.7 on 2023-03-24 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_delete_news_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='%d %m %y/profile.png', upload_to='uploads'),
        ),
    ]
