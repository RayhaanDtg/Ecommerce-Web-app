# Generated by Django 3.1.2 on 2021-03-21 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CartItem', '0002_auto_20210320_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='subtotal',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
        ),
    ]