from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.ProductListView.as_view(), name='product-list-page'),
    path('products/brand/<str:brand>/', views.ProductListView.as_view(), name='product-brand-list'),
    path('products/car/<str:car>/', views.ProductListView.as_view(), name='product-car-list'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),
]
