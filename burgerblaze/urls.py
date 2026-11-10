"""
URL configuration for burgerblaze project.
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from restaurant.views import (
    MenuViewSet, CategoryViewSet, OrderViewSet, 
    CartViewSet, home_view, register_view, account_view
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
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('accounts/register/', register_view, name='register'),
    path('account/', account_view, name='account'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
