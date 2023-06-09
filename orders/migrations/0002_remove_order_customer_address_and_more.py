# Generated by Django 4.2 on 2023-04-06 20:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer_email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer_phone',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='customers.customer'),
        ),
    ]
