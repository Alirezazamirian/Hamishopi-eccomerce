# Generated by Django 5.0.2 on 2024-03-18 20:15

import account_module.forms
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_module', '0004_orderformclass_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderformclass',
            name='followup_code',
            field=models.PositiveIntegerField(blank=True, default=12345678910123, verbose_name='کد پیگیری'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orderformclass',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True, validators=[account_module.forms.validate_phone_number_startswith_09], verbose_name='شماره سفارش دهنده'),
        ),
    ]