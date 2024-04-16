# Here we will create the urls of the app

from django.urls import path
from . import views

urlpatterns = [
    # home page url
    path('', views.home, name='home'),
    
    # seller/user login page urls
    path('seller/', views.sellerIntro, name='sellerIntro'),
    path('sellerLogin/', views.sellerLogin, name='sellerLogin'),
    path('sellerLoginSubmit/', views.sellerLoginSubmit, name='sellerLoginSubmit'),
    path('sellerAccount/', views.sellerAccount, name='sellerAccount'),
    path('saveSellerProfile/', views.saveSellerProfile, name='saveSellerProfile'),
    path('sellerProducts/', views.sellerProducts, name='sellerProducts'),
    
    path('userLogin/', views.userLogin, name='userLogin'),
    path('userLoginSubmit/', views.userLoginSubmit, name='userLoginSubmit'),
    path('createUserProfile', views.createUserProfile, name="createUserProfile"),
    path('saveUserProfile/', views.saveUserProfile, name='saveUserProfile'),

    # user/seller logout urls
    path('logout/', views.userLogout, name='userLogout'),
    path("sellerLogout/", views.sellerLogout, name="sellerLogout"),
    
    # product page urls
    path('category_Products/<str:product_category>', views.category_Products, name='category_Products'),
    path('product_Details/<str:id>', views.product_Details, name='product_Details'),
    path('purchase_product/<str:id>/<str:net_product_amount>', views.purchase_product, name="purchase_product"),
    
    # cart page urls
    path('add_to_cart/<str:product_name>/<str:product_desc>', views.add_to_cart, name="add_to_cart"),
    path('cart', views.cart, name="cart"),
    
    # some other urls
    path('purchase/<str:product_desc>/<str:text>', views.purchase, name="purchase"),
    path("purchase_product/<str:product_desc>/<int:net_product_amount>", views.purchase_product, name="purchase_product"),
    
    path('remove_Product/<str:id>', views.remove_Product, name='remove_Product'),
    
    path('cart_product_detail/<str:id>', views.cart_product_detail, name='cart_product_detail'),
    
    path('myaccount/', views.myaccount, name='myaccount'),
    path('myorders/', views.myorders, name="myorders"),

    path('seller_progress_Details/<str:id>', views.seller_progress_Details, name="seller_progress_Details")
]
