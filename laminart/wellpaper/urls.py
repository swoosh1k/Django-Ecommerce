from django.contrib.auth.views import LogoutView
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from .views import *

urlpatterns = [
    path('', index, name = 'index'),
    path('wellpaper/login/', UserLogin.as_view(), name = 'login'),
    path('register/', UserRegister.as_view(), name = 'register'),
    path('logout/', LogoutView.as_view(), name  = 'logout'),
    path('add_to_cart/<int:pk>/', add_to_cart, name = 'add_to_cart'),
    path('cart/', user_cart , name = 'cart'),
    path('create_order/', create_order, name = 'create_order'),
    path('delete_item/<int:pk>/', delete_item, name = 'delete_item')
]






urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
