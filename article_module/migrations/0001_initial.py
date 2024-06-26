# Generated by Django 5.0.2 on 2024-03-03 21:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='عنوان دسته بندی')),
                ('url_title', models.CharField(max_length=200, unique=True, verbose_name='عنوان در url')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال / غیرفعال')),
            ],
            options={
                'verbose_name': 'دسته بندی مقاله',
                'verbose_name_plural': 'دسته بندی های مقاله',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300, verbose_name='عنوان مقاله')),
                ('slug', models.SlugField(allow_unicode=True, max_length=400, verbose_name='عنوان در url')),
                ('image', models.ImageField(upload_to='images/articles', verbose_name='تصویر مقاله')),
                ('short_description', models.TextField(verbose_name='توضیحات کوتاه')),
                ('text', models.TextField(verbose_name='متن مقاله')),
                ('is_active', models.BooleanField(default=True, verbose_name='فعال / غیرفعال')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('selected_categories', models.ManyToManyField(to='article_module.articlecategory', verbose_name='دسته بندی ها')),
            ],
            options={
                'verbose_name': 'مقاله',
                'verbose_name_plural': 'مقالات',
            },
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='نام خانوادگی')),
                ('create_date', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('text', models.TextField(verbose_name='متن نظر')),
                ('is_okay', models.BooleanField(default=False, verbose_name='مورد تایید')),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='article_module.article', verbose_name='مقاله')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'نظر مقاله',
                'verbose_name_plural': 'نظرات مقاله',
            },
        ),
    ]
