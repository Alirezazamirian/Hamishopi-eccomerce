# Generated by Django 5.0.2 on 2024-03-04 02:18

import account_module.forms
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_module', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderFormClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='نام سفارش دهنده')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='نام خانوادگی سفارش دهنده')),
                ('province', models.CharField(blank=True, max_length=30, verbose_name='استان سفارش دهنده')),
                ('city', models.CharField(blank=True, max_length=30, verbose_name='شهر سفارش دهنده')),
                ('address', models.TextField(blank=True, max_length=200, verbose_name='آدرس سفارش دهنده')),
                ('postal_code', models.CharField(blank=True, max_length=30, verbose_name='کد پستی سفارش دهنده')),
                ('phone', models.CharField(blank=True, max_length=30, validators=[account_module.forms.validate_phone_number_startswith_09], verbose_name='شماره سفارش دهنده')),
                ('instagram', models.CharField(blank=True, max_length=30, null=True, verbose_name='ایدی اینستا سفارش دهنده')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سفارش کاربر',
                'verbose_name_plural': 'سفارشات کاربران',
            },
        ),
    ]