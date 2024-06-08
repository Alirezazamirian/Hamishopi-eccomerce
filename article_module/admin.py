from django.contrib import admin
from django.http import HttpRequest

from . import models

# Register your models here.
from .models import Article


class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'is_active']
    list_editable = ['url_title', 'is_active']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active']
    list_editable = ['is_active']

    def save_model(self, request: HttpRequest, obj: Article, form, change):
        if not change:
            obj.author = request.user
        return super().save_model(request, obj, form, change)


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'create_date', 'is_okay']


admin.site.register(models.ArticleCategory, ArticleCategoryAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.ArticleComment, ArticleCommentAdmin)
