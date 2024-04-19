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
    path('cart/', user_cart , name = 'cart'),
    path('create_order/', create_order, name = 'create_order'),
    path('add_product_in_cart/', add_product_in_cart, name = 'add_product_in_cart'),
    path('update_cart/', update_cart, name='update_cart'),
    path('about_us/', about_us, name = 'about_us'),
    path('generate/', generate, name= 'generate'),
    path('filter-products/', filter_products, name = 'filter-products'),
    path('parsing/', parsing, name = 'parsing'),
    path('product_detail/<int:pk>/', product_detail, name = 'product_detail' )
]






urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
