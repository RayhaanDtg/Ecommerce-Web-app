# Generated by Django 3.1.2 on 2021-01-12 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_remove_address_address_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_id',
            field=models.CharField(blank=True, max_length=120),
        ),
    ]