from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import DetailView, CreateView, TemplateView, FormView
from django.views.generic.list import ListView

from article_module.models import Article, ArticleCategory, ArticleComment


class ArticlesListView(ListView):
    model = Article
    paginate_by = 4
    template_name = 'article_module/article_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticlesListView, self).get_context_data(*args, **kwargs)
        article_main_categories = ArticleCategory.objects.filter(is_active=True)
        context['main_categories'] = article_main_categories
        return context

    def get_queryset(self):
        query = super(ArticlesListView, self).get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_categories__url_title__iexact=category_name)
        return query


class ArticleDetailView(DetailView):
    template_name = 'article_module/article_detail.html'
    model = Article

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        articles: Article = self.kwargs.get('pk')
        context['comments'] = ArticleComment.objects.filter(article_id=articles, is_okay=True).order_by(
            '-create_date')

        context['comments_count'] = ArticleComment.objects.filter(article_id=articles, is_okay=True).count()
        context['articles'] = articles
        return context


def error(request):
    return render(request, 'article_module/video_list.html', {})
