# Generated by Django 5.0.2 on 2024-03-03 21:54

import account_module.forms
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
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
                ('is_paid', models.BooleanField(default=False, verbose_name='نهایی شده/نشده')),
                ('payment_date', models.DateField(blank=True, null=True, verbose_name='تاریخ پرداخت')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سبد خرید',
                'verbose_name_plural': 'سبدهای خرید کاربران',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_price', models.IntegerField(blank=True, null=True, verbose_name='قیمت نهایی تکی محصول')),
                ('count', models.IntegerField(verbose_name='تعداد')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_module.order', verbose_name='سبد خرید')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_app.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'جزییات سبد خرید',
                'verbose_name_plural': 'لیست جزییات سبدهای خرید',
            },
        ),
    ]
