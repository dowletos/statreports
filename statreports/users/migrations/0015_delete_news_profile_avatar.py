# Generated by Django 4.1.7 on 2023-03-24 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_delete_updateusersdatamodel_alter_userrights_userid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='News',
        ),
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='profile.png', upload_to='uploads'),
        ),
    ]
