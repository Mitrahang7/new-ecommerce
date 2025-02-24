from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class Category(models.Model):
  name=models.CharField(max_length=20)

  class Meta:
    verbose_name_plural= 'Categories'

  def __str__(self):
    return self.name


class Product(models.Model):
  name= models.CharField(max_length=30)
  category= models.ForeignKey(Category, on_delete=models.CASCADE)
  price= models.DecimalField(default=0, decimal_places=2, max_digits=6)
  description=models.TextField()
  image= models.ImageField(upload_to='uploads/product/')
  is_sale= models.BooleanField(default=False)
  sale_price= models.DecimalField(default=0, decimal_places=2, max_digits=6)

  def __str__(self):
    return self.name
  

class Profile(models.Model):
  user= models.OneToOneField(User, on_delete=models.CASCADE)
  address1= models.CharField(max_length=200, blank=True)
  address2= models.CharField(max_length=200, blank=True)
  phone= models.CharField(max_length=20, blank=True)
  disrtict= models.CharField(max_length=200, blank=True)
  province= models.CharField(max_length=200, blank=True)


  def __str__(self):
    return self.user.username
  

def create_profile(sender, instance, created, **kwargs):
  if created:
    user_profile=Profile(user=instance)
    user_profile.save()

post_save.connect(create_profile, sender=User)

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    shipped_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"