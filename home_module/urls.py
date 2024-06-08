from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('about-us/', views.AboutPage.as_view(), name='about_page')
]
