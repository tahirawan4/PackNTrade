from django.contrib import admin
from trade.models import Product, Category, Order, OrderDetail, Payment, PromoCode, ProductPurchased, WishList

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(OrderDetail)
admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(ProductPurchased)
admin.site.register(WishList)
admin.site.register(PromoCode)