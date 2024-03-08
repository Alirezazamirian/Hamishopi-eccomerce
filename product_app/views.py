from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse, resolve
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Product, ProductVisit, ProductGallery, Brand, Car
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


class ProductDetailView(DetailView):
    template_name = 'product_app/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        request = self.request
        favorite_product_id = request.session.get("product_favorites")
        context['is_favorite'] = favorite_product_id == str(loaded_product.id)
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
