import datetime

from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, CreateView, TemplateView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django.views.generic.list import ListView
from django.contrib import messages
from account_module.models import User
from article_module.forms import ArticleCommentForm
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


class CommentGet(DetailView):
    model = Article
    template_name = 'article_module/article_detail.html'

    def get_queryset(self):
        query = super(CommentGet, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = ArticleCommentForm()
        articles: Article = self.kwargs.get('pk')
        context['comments'] = ArticleComment.objects.filter(article_id=articles, is_okay=True).order_by(
            '-create_date')
        context['comments_count'] = ArticleComment.objects.filter(article_id=articles, is_okay=True).count()

        return context


class ArticleDetailView(View):

    def get(self, request, *args, **kwargs):
        view = CommentGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        messages.success(request, "نظر شما با موفقیت ثبت شد و بعد از تایید نمایش داده میشود ")
        return view(request, *args, **kwargs)


class CommentPost(SingleObjectMixin, FormView):
    model = Article
    form_class = ArticleCommentForm
    template_name = "article_module/article_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.article = self.object
        comment.user = self.request.user
        existed_user: User = User.objects.get(pk=self.request.user.id)
        existed_user.first_name = comment.first_name
        existed_user.last_name = comment.last_name
        existed_user.save()
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse("articles_detail", kwargs={'pk': post.pk})



def error(request):
    return render(request, 'article_module/video_list.html', {})
