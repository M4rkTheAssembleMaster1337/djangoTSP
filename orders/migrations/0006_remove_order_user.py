# Generated by Django 4.2 on 2023-04-07 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='user',
        ),
    ]
