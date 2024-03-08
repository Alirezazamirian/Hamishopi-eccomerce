from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home_module.urls')),
    path('', include('account_module.urls')),
    path('', include('product_app.urls')),
    path('articles/', include('article_module.urls')),
    path('contact-us/', include('contact_module.urls')),
    path('user/', include('user_panel.urls')),
    path('order/', include('order_module.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
