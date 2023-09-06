from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Type(models.Model):
    name = models.CharField(max_length=20)
    
    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=40)
    
    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=30)
   
    def __str__(self):
        return self.name

class Product(models.Model):
    brand = models.CharField(max_length=40)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.IntegerField()
    purchases = models.IntegerField()
    stock = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.brand

    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.product, self.user
    
    class Meta:
        ordering = ['-created']
        


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    