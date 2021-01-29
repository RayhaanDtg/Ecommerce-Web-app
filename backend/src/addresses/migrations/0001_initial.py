# Generated by Django 3.1.2 on 2021-01-08 07:46

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('BillingProfile', '0002_auto_20201223_0202'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_line_1', models.CharField(max_length=120)),
                ('address_type', models.CharField(choices=[('shipping', 'Shipping'), ('billing', 'Billing')], max_length=120)),
                ('city', models.CharField(max_length=120)),
                ('state', models.CharField(max_length=120)),
                ('zip_code', models.CharField(max_length=120)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('billing_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='BillingProfile.billingprofile')),
            ],
        ),
    ]