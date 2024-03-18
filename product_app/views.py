from django.contrib import messages
from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, resolve
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.base import View
from django.views.generic.detail import SingleObjectMixin

from account_module.models import User
from .forms import ProductCommentForm
from .models import Product, ProductVisit, ProductGallery, Brand, Car, ProductComment
from utils.http_service import get_client_ip
from utils.convertors import group_list


class ProductListView(ListView):
    template_name = 'product_app/product_list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        cars: Car = Car.objects.filter(is_active=True, is_delete=False)
        context['cars'] = cars
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        car = self.kwargs.get('car')
        brand = self.kwargs.get('brand')

        if car is not None:
            query = query.filter(car__url_title__iexact=car)

        if brand is not None:
            query = query.filter(brand__url_title__iexact=brand)
        return query


class ProductDetailView(View):

    def get(self, request, *args, **kwargs):
        second_view = CommentGet.as_view()
        return second_view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = CommentPost.as_view()
        messages.success(request, "نظر شما با موفقیت ثبت شد و بعد از تایید نمایش داده میشود ")
        return view(request, *args, **kwargs)


class CommentGet(DetailView):
    model = Product
    template_name = 'product_app/product_detail.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["form"] = ProductCommentForm()
        product: Product = self.kwargs.get('slug')
        selected_product = Product.objects.get(slug=product)
        comments = ProductComment.objects.filter(product__slug__iexact=product, is_okay=True).order_by(
            '-create_date')
        context['comments'] = comments
        context['comments_count'] = ProductComment.objects.filter(product__slug__iexact=product, is_okay=True).count()
        five_score = 0
        for content in comments:
            if content.score == 5:
                five_score = five_score + 1
        context['five_score'] = five_score
        four_score = 0
        for content in comments:
            if content.score == 4:
                four_score = four_score + 1
        context['four_score'] = four_score
        three_score = 0
        for content in comments:
            if content.score == 3:
                three_score = three_score + 1
        context['three_score'] = three_score
        two_score = 0
        for content in comments:
            if content.score == 2:
                two_score = two_score + 1
        context['two_score'] = two_score
        one_score = 0
        for content in comments:
            if content.score == 1:
                one_score = one_score + 1
        context['one_score'] = one_score

        if comments.exists():
            if selected_product.avg_rating == 0:
                selected_product.avg_rating = ProductComment.objects.first().score
                # selected_product.number_rating = selected_product.number_rating + 1

            else:
                avg = 0
                n = 0
                m = 0
                for review in comments:
                    n = review.score + n
                    m = m + 1
                    avg = n / m
                selected_product.avg_rating = avg
                # selected_product.number_rating = selected_product.number_rating + 1
            selected_product.save()

        loaded_product = self.object
        galleries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galleries.insert(0, loaded_product)
        context['product_galleries_group'] = group_list(galleries, 3)
        context['related_products'] = group_list(
            list(Product.objects.filter(car_id=loaded_product.car_id).exclude(pk=loaded_product.id).all()[:15]), 3)
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id

        has_been_visited = ProductVisit.objects.filter(ip__iexact=user_ip, product_id=loaded_product.id).exists()

        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()

        return context


class CommentPost(SingleObjectMixin, FormView):
    model = Product
    form_class = ProductCommentForm
    template_name = "product_app/product_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.product = self.object
        comment.user = self.request.user
        existed_user: User = User.objects.get(pk=self.request.user.id)
        existed_user.first_name = comment.first_name
        existed_user.last_name = comment.last_name
        existed_user.save()
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        post = self.get_object()
        return reverse("product-detail", kwargs={'slug': post.slug})
