# Generated by Django 3.1.2 on 2021-03-01 10:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0002_remove_address_country'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='zip_code',
            new_name='address_line_2',
        ),
    ]