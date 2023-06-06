from django.contrib import admin
from .models import sellerProduct,UserProfile

@admin.register(sellerProduct)
class SellerAdmin(admin.ModelAdmin):
    list_display=['seller','product']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display=['user','is_owner']


