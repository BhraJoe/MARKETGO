from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), path('shop/', views.shop, name='shop'), path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('sell/', views.create_product, name='create_product'), path('favorite/<uuid:product_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('cart/', views.cart, name='cart'), path('cart/add/<uuid:product_id>/', views.add_to_cart, name='add_to_cart'), path('cart/remove/<uuid:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'), path('orders/', views.orders, name='orders'), path('contact/', views.contact, name='contact'), path('safety/', views.safety, name='safety'), path('policies/', views.policies, name='policies'), path('accounts/login/', views.login_view, name='login'), path('accounts/register/', views.register_view, name='register'), path('accounts/logout/', views.logout_view, name='logout'),
]
