# Generated by Django 3.1.2 on 2020-12-03 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20201121_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(default='abc', unique=True),
            preserve_default=False,
        ),
    ]
