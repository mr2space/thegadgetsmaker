# Generated by Django 4.1.7 on 2023-02-28 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0002_rename_payment_status_paymentinfo_payment_completed'),
    ]

    operations = [
        migrations.CreateModel(
            name='FailedPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.CharField(max_length=200)),
                ('user', models.CharField(max_length=200)),
                ('payment_id', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]