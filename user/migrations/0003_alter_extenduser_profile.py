# Generated by Django 4.1.7 on 2023-03-07 17:06

from django.db import migrations, models
import user.models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_extenduser_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extenduser',
            name='profile',
            field=models.ImageField(default='hacker.png', upload_to=user.models.imgFolder),
        ),
    ]
