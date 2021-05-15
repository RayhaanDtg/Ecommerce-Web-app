# Generated by Django 3.1.2 on 2021-02-05 08:16

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('image', models.ImageField(blank=True, null=True, upload_to=products.models.upload_img)),
                ('InStock', models.BooleanField(default=False)),
            ],
        ),
    ]
