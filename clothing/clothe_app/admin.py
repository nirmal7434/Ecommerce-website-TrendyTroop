from django.contrib import admin

from .models import Category, Product,Size,Review,ProductSize,Cart,Wishlist,Order,OrderItem,PromoCode

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Size)
admin.site.register(Review)
admin.site.register(ProductSize)
admin.site.register(Cart)
admin.site.register(Wishlist)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(PromoCode)
