# Generated by Django 4.1.7 on 2023-03-01 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_alter_course_title_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='meet_link',
            field=models.CharField(default=None, max_length=140),
        ),
    ]
