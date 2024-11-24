# Generated by Django 5.1.3 on 2024-11-24 09:39

import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=60)),
                ('title_img', models.ImageField(default='hacker.png', upload_to='courses/img')),
                ('short_des', models.CharField(max_length=150)),
                ('description', tinymce.models.HTMLField()),
                ('price', models.FloatField()),
                ('course_time', models.DateTimeField()),
                ('meet_link', models.CharField(max_length=140, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
