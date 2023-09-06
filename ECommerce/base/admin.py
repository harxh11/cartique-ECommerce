from django.contrib import admin
from .models import Type, Category, Product, Brand, Review, Wishlist, Cart
# Register your models here.


admin.site.register(Type)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Cart)