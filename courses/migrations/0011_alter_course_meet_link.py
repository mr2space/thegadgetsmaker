# Generated by Django 4.1.7 on 2023-03-02 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_course_meet_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='meet_link',
            field=models.CharField(default=' ', max_length=140, null=True),
        ),
    ]
