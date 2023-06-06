from django.db import models
from shop.models import Product
from django.contrib.auth.models import User

# Create your models here.
class sellerProduct(models.Model):
    seller=models.ForeignKey(User,related_name='seller',on_delete=models.CASCADE)
    product=models.ForeignKey(Product,related_name='product',on_delete=models.CASCADE)
    def __str__(self):
        return self.owner.username
    
class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='userprofile',on_delete=models.CASCADE)
    is_owner=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username