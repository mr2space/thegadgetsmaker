# Generated by Django 4.1.7 on 2023-02-28 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='paymentinfo',
            old_name='payment_status',
            new_name='payment_completed',
        ),
    ]