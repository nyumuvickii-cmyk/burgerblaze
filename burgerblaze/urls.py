"""
URL configuration for burgerblaze project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from restaurant.views import (
    MenuViewSet, CategoryViewSet, OrderViewSet, 
    CartViewSet, home_view
)

router = DefaultRouter()
router.register(r'menu', MenuViewSet, basename='menu')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('', home_view, name='home'),
    path('menu/', TemplateView.as_view(template_name='menu.html'), name='menu'),
    path('order/', TemplateView.as_view(template_name='order.html'), name='order'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
