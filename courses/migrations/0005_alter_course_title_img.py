# Generated by Django 4.1.7 on 2023-02-28 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_course_title_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='title_img',
            field=models.ImageField(default='hacker.png', upload_to='courses/img'),
        ),
    ]
