from django.contrib import admin
from .models import Category,Product,Profile,Order,OrderItem
from django.contrib.auth.models import User

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderItem)


class ProfileInline(admin.StackedInline):
  model = Profile

class UserAdmin(admin.ModelAdmin):
  model = User
  fields = ['username', 'first_name', 'last_name', 'email']
  inlines = [ProfileInline]

admin.site.unregister(User)

admin.site.register(User, UserAdmin)