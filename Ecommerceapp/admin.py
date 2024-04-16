from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Product)
admin.site.register(ProductCategory)

admin.site.register(UserCart)
admin.site.register(UserLogin)
admin.site.register(UserProfile)
admin.site.register(UserOrder)

admin.site.register(SellerLogin)
admin.site.register(SellerProfile)